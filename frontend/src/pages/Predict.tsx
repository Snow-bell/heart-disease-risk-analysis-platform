import { useState } from 'react';
import client from '../api/client';

interface PredictionResult {
  heart_disease_present: number;
  risk_probability: number;
  risk_percentage: number;
}

function Predict() {
  const [form, setForm] = useState({
    age: '',
    sex: '1',
    trestbps: '',
    chol: '',
    fbs: '0',
    thalach: '',
    exang: '0',
    oldpeak: '',
    ca: '',
    cp: 'typical angina',
    restecg: 'normal',
    slope: 'flat',
    thal: 'normal',
  });

  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await client.post('/api/predict', {
        ...form,
        age: parseInt(form.age),
        sex: parseInt(form.sex),
        trestbps: parseInt(form.trestbps),
        chol: parseInt(form.chol),
        fbs: parseInt(form.fbs),
        thalach: parseInt(form.thalach),
        exang: parseInt(form.exang),
        oldpeak: parseFloat(form.oldpeak),
        ca: parseInt(form.ca),
      });
      setResult(res.data);
    } catch (err) {
      setError('Failed to get prediction. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-blue-900 mb-6">Heart Disease Risk Prediction</h1>

      <div className="bg-white rounded-lg shadow p-6 max-w-2xl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <div>
            <label className="block text-sm text-slate-600 mb-1">Age</label>
            <input name="age" type="number" value={form.age} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm" />
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Sex</label>
            <select name="sex" value={form.sex} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm">
              <option value="1">Male</option>
              <option value="0">Female</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Resting Blood Pressure</label>
            <input name="trestbps" type="number" value={form.trestbps} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm" />
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Cholesterol</label>
            <input name="chol" type="number" value={form.chol} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm" />
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Fasting Blood Sugar &gt; 120mg/dl</label>
            <select name="fbs" value={form.fbs} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm">
              <option value="0">No</option>
              <option value="1">Yes</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Max Heart Rate</label>
            <input name="thalach" type="number" value={form.thalach} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm" />
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Exercise Induced Angina</label>
            <select name="exang" value={form.exang} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm">
              <option value="0">No</option>
              <option value="1">Yes</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">ST Depression (Oldpeak)</label>
            <input name="oldpeak" type="number" step="0.1" value={form.oldpeak} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm" />
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Major Vessels (CA)</label>
            <input name="ca" type="number" min="0" max="3" value={form.ca} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm" />
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Chest Pain Type</label>
            <select name="cp" value={form.cp} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm">
              <option value="typical angina">Typical Angina</option>
              <option value="atypical angina">Atypical Angina</option>
              <option value="non-anginal">Non-anginal</option>
              <option value="asymptomatic">Asymptomatic</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Resting ECG</label>
            <select name="restecg" value={form.restecg} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm">
              <option value="normal">Normal</option>
              <option value="st-t abnormality">ST-T Abnormality</option>
              <option value="lv hypertrophy">LV Hypertrophy</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Slope</label>
            <select name="slope" value={form.slope} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm">
              <option value="upsloping">Upsloping</option>
              <option value="flat">Flat</option>
              <option value="downsloping">Downsloping</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-600 mb-1">Thalassemia</label>
            <select name="thal" value={form.thal} onChange={handleChange}
              className="w-full border rounded px-3 py-2 text-sm">
              <option value="normal">Normal</option>
              <option value="fixed defect">Fixed Defect</option>
              <option value="reversable defect">Reversable Defect</option>
            </select>
          </div>

        </div>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="mt-6 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {loading ? 'Predicting...' : 'Get Prediction'}
        </button>

        {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}

        {result && (
          <div className={`mt-6 p-4 rounded-lg ${
            result.heart_disease_present > 0 ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'
          }`}>
            <p className="text-lg font-semibold mb-2">
              {result.heart_disease_present > 0 ? '⚠️ Heart Disease Risk Detected' : '✅ Low Heart Disease Risk'}
            </p>
            <p className="text-sm text-gray-600">Risk Probability: <span className="font-medium">{result.risk_percentage}%</span></p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Predict;