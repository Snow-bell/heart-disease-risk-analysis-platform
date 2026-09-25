import { useEffect, useState } from 'react';
import client from '../api/client';

interface Summary {
  total_patients: number;
  with_heart_disease: number;
  without_heart_disease: number;
  heart_disease_percentage: number;
  avg_age: number;
  avg_cholesterol: number;
  avg_blood_pressure: number;
}

function Dashboard() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    client.get('/api/stats/summary')
      .then(res => setSummary(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-gray-500">Loading...</p>;
  if (!summary) return <p className="text-red-500">Failed to load summary.</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold text-blue-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-900">Total Patients</p>
          <p className="text-3xl font-bold text-slate-800">{summary.total_patients}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-900">With Heart Disease</p>
          <p className="text-3xl font-bold text-red-500">{summary.with_heart_disease}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-900">Without Heart Disease</p>
          <p className="text-3xl font-bold text-green-500">{summary.without_heart_disease}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-900">Heart Disease Rate</p>
          <p className="text-3xl font-bold text-gray-800">{summary.heart_disease_percentage}%</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-900">Average Age</p>
          <p className="text-3xl font-bold text-gray-800">{summary.avg_age}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-900">Average Cholesterol</p>
          <p className="text-3xl font-bold text-gray-800">{summary.avg_cholesterol}</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;