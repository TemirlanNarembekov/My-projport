# Детекция аномальных новостей в потоке погодных сообщений

В ноутбуке anomaly_notebook.ipynb представлено обучение модели, которая выявляет аномальные новости (мира, ЧП и тд) среди потока допустимых прогнозов погоды и помечает любое сообщение, не похожее на погоду, как аномалию. Использует ансамбль sentence-transformers энкодеров, UMAP для снижения размерности и HDBSCAN для кластеризации с подбором гиперпараметров через Optuna.
Так же приложен pipeline в котором лежат обученные модели HDBSCAN И UMAP. В ноутбуке dover_intervals.ipynb показано их загрузка.
## Результаты

На тестовой выборке с порогом, подобранным на валидации:

| Метрика | Значение |
|---|---|
| Recall | 98% |
| Precision | 46% |
| F1 | 0.62 |
| TP / Всего аномалий | 49 / 50 |
| FP | 58 |
| FN | 1 |

В рамках оценки качества модели на Тестовой выборке, на иференс было подано 1472 прогнозов погоды + 50 аномальных новостей, с разметкой.
Из 50 настоящих аномальных новостей модель поймала 49. Цена этого — 58 ложных тревог(модель приняла погодные сообщения за аномалии).

## Архитектура пайплайна

```
[Тексты] → [3 энкодера] → [L2 норма] → [UMAP 2D × 3] → [Конкатенация 3 разных эмбеддингов в один 6мерный вектор]
                                                            ↓
                                                       [HDBSCAN по Тренировочной выборке состаящей только из погодных сообщений]
                                                            ↓
                                              [strength для каждой точки; strength подобран на валидационной выборке с разметкой]
                                                            ↓
                                              [strength < threshold = аномалия]
```

**Энкодеры** (ансамбль из 3 моделей):
- `all-MiniLM-L6-v2`
- `cointegrated/rubert-tiny2`
- `paraphrase-multilingual-mpnet-base-v2`

Каждая модель кодирует тексты независимо, затем UMAP сжимает каждый набор эмбеддингов в 2D, и три проекции конкатенируются в финальный 6D вектор.

**HDBSCAN** обучается только на погодных данных и строит кластеры «нормы». Для новых сообщений алгоритм возвращает `strength` — уверенность принадлежности к ближайшему кластеру. Низкий strength = сообщение не похоже на погоду = аномалия.

## Источники данных

- **Погода** — Open-Meteo API (открытый, без ключа), 20 городов России, 46 дней (16 forecast + 30 past), шаг 3 часа = ~7400 сообщений
- **Аномалии** — корпус новостей Lenta.ru ([Kaggle dataset](https://www.kaggle.com/datasets/yutkin/corpus-of-russian-news-articles-from-lenta)), отфильтровано по ключевым словам (происшествия, катастрофы, чрезвычайные ситуации, война, конфликт, авария)

## Разбиение данных

```
Погода (7400 сообщений с shuffle):
  Train: 40% — обучение HDBSCAN
  Val:   40% — подбор гиперпараметров и порога
  Test:  20% — финальная оценка

Аномалии:
  Val:  150 сообщений
  Test: 50 сообщений
```

Train/val/test погодных не пересекаются, аномалии тоже разделены без пересечений.

## Подбор гиперпараметров

Optuna с TPE sampler и Hyperband pruner, 5000 trials, целевая метрика — F1.

Перебираемые параметры HDBSCAN:
- `min_cluster_size`: 20-300
- `min_samples`: 1-20
- `cluster_selection_epsilon`: 0.0-1.0
- `cluster_selection_persistence`: 0.0-1.0
- `metric`: euclidean / manhattan
- `alpha`: 0.5-1.5
- `cluster_selection_method`: eom / leaf
- `allow_single_cluster`: True / False

Для оценки используется 3-fold кросс-валидация: HDBSCAN обучается на 2 фолдах train, валидируется на оставшемся фолде train + соответствующей части размеченной валидации. Для каждого fold внутри trial перебирается порог `strength` от 0.05 до 0.5, выбирается лучший F1.

После optimization порог финализируется отдельным перебором на полной валидационной выборке без подглядывания в test, чтобы избежать data leakage.

## Установка

Требуется Python 3.9+.

```bash
pip install requests numpy pandas matplotlib
pip install scikit-learn hdbscan umap-learn
pip install sentence-transformers
pip install optuna joblib
```

## Подготовка датасета аномалий

Скачайте корпус новостей Lenta.ru с Kaggle:
https://www.kaggle.com/datasets/yutkin/corpus-of-russian-news-articles-from-lenta

Положите файл `lenta-ru-news.csv` в корневую директорию проекта (рядом с ноутбуком).

## Запуск

Откройте `anomaly_notebook.ipynb` в Jupyter / VS Code и выполняйте ячейки по порядку:

1. **Импорты** — все необходимые библиотеки
2. **Конфигурация** — список городов, словарь погодных явлений, функции загрузки и очистки текста
3. **Загрузка аномалий** — фильтрация заголовков из Lenta.ru
4. **Загрузка погоды** — запросы к Open-Meteo, shuffle, разбиение на train/val/test
5. **Загрузка энкодеров** — три sentence-transformers модели
6. **Векторизация** — кодирование, L2-нормализация, UMAP, конкатенация в 6D
7. **Optuna optimization** — подбор гиперпараметров HDBSCAN (5000 trials, ~30-60 минут на CPU)
8. **Финальное обучение** — HDBSCAN с лучшими параметрами на полном train
9. **Подбор порога** — на валидации, по F1
10. **Финальная оценка** — на тесте с зафиксированным порогом
11. **Анализ ошибок** — вывод FN и FP для понимания где модель ошибается
12. **Сохранение** — модель сохраняется через joblib

Запуск без GPU. Самые тяжёлые этапы — векторизация (5-10 минут на CPU) и Optuna (30-60 минут).

## Структура проекта

```
.
├── anomaly_notebook.ipynb        # основной ноутбук
├── lenta-ru-news.csv             # датасет аномалий (скачать с Kaggle)
├── HDBSCAN_F1_optimized_v1.0.pkl # сохранённая обученная модель
└── README.md
```

## Использование сохранённой модели для инференса

```python
import joblib
import hdbscan

clusterer = joblib.load("HDBSCAN_F1_optimized_v1.0.pkl")

# new_embeddings — 6D эмбеддинги новых сообщений (тот же пайплайн векторизации)
_, strengths = hdbscan.approximate_predict(clusterer, new_embeddings)
predictions = (strengths < best_threshold).astype(int)
# 1 = аномалия, 0 = норма
```


## Используемые библиотеки

- [sentence-transformers](https://github.com/UKPLab/sentence-transformers) — энкодеры
- [umap-learn](https://github.com/lmcinnes/umap) — снижение размерности
- [hdbscan](https://github.com/scikit-learn-contrib/hdbscan) — кластеризация
- [optuna](https://github.com/optuna/optuna) — оптимизация гиперпараметров
- [Open-Meteo](https://open-meteo.com/) — погодный API
