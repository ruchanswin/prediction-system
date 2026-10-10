from pathlib import Path

import joblib
import numpy as np
import onnxruntime as ort
import onnxmltools
from onnxmltools.convert.common.data_types import FloatTensorType


backend_dir = Path(__file__).resolve().parent
model_path = backend_dir / "model" / "lgbm_regressor_delay.pkl"
onnx_path = backend_dir / "model" / "delay_regressor.onnx"

model = joblib.load(model_path)
initial_types = [
    ("features", FloatTensorType([None, model.n_features_in_])),
]
onnx_model = onnxmltools.convert_lightgbm(model, initial_types=initial_types)
onnx_path.write_bytes(onnx_model.SerializeToString())

session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
sample = np.zeros((1, model.n_features_in_), dtype=np.float32)
expected = np.asarray(model.predict(sample)).reshape(-1)
actual = np.asarray(
    session.run(None, {session.get_inputs()[0].name: sample})[0]
).reshape(-1)
np.testing.assert_allclose(actual, expected, rtol=1e-5, atol=1e-5)

print(f"Exported and validated delay model: {onnx_path}")
