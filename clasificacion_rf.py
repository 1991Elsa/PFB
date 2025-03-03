from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import col
import pickle
from tratamiento_nans import  tratamiento_nans_historic, tratamiento_nans_info

nasdaq_tickers_info = tratamiento_nans_info()
nasdaq_tickers_historic = tratamiento_nans_historic()

def modelo_clasificacion(df, target_colum):
    
    features = [col for col in df.columns if col not in []]
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    df_assembled = assembler.transform(df)

    scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
    df_scaled = scaler.fit(df_assembled).transform(df_assembled)

    with open('modelo_clasificacion.pkl', 'wb') as file:
        pickle.dump(scaler, file)

    train_data, test_data = df_scaled.randomSplit([0.8, 0.2], seed=42)

    rf_model = RandomForestClassifier(labelCol=target_colum, featuresCol="scaled_features", numTrees=100, seed=42)

    rf_model_trained = rf_model.fit(train_data)

    predictions = rf_model_trained.transform(test_data)

    evaluator = MulticlassClassificationEvaluator(labelCol=target_colum, predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    print(f"Accuracy: {accuracy:.4f}")

    with open('modelo_clasificacion.pkl', 'wb') as file:
        pickle.dump(rf_model_trained, file)

    return rf_model_trained, scaler

rf_model, scaler = modelo_clasificacion(nasdaq_tickers_info, nasdaq_tickers_historic)