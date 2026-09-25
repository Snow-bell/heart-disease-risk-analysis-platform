import { useEffect, useState } from 'react';
import client from '../api/client';

interface SexStat {
  sex: string;
  total: number;
  with_disease: number;
}

interface ThalStat {
  thal_type: string;
  total: number;
  with_disease: number;
}

interface RiskFactor {
  heart_disease_present: number;
  avg_cholesterol: number;
  avg_blood_pressure: number;
  avg_max_heart_rate: number;
  avg_age: number;
}

function Stats() {
  const [sexStats, setSexStats] = useState<SexStat[]>([]);
  const [thalStats, setThalStats] = useState<ThalStat[]>([]);
  const [riskFactors, setRiskFactors] = useState<RiskFactor[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      client.get('/api/stats/by-sex'),
      client.get('/api/stats/by-thal'),
      client.get('/api/stats/risk-factors'),
    ]).then(([sexRes, thalRes, riskRes]) => {
      setSexStats(sexRes.data);
      setThalStats(thalRes.data);
      setRiskFactors(riskRes.data);
    }).catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold text-blue-900 mb-6">Statistics</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 style={{color: '#0f172a'}} className="text-lg font-semibold mb-4">By Sex</h2>
          <table className="w-full text-sm text-slate-900">
            <thead className="text-slate-500 uppercase text-xs">
              <tr>
                <th className="text-left py-2">Sex</th>
                <th className="text-left py-2">Total</th>
                <th className="text-left py-2">With Disease</th>
                <th className="text-left py-2">Rate</th>
              </tr>
            </thead>
            <tbody>
              {sexStats.map(s => (
                <tr key={s.sex} className="border-t">
                  <td className="py-2">{s.sex}</td>
                  <td className="py-2">{s.total}</td>
                  <td className="py-2">{s.with_disease}</td>
                  <td className="py-2">{Math.round(s.with_disease / s.total * 100)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 style={{color: '#0f172a'}} className="text-lg font-semibold mb-4">By Thalassemia Type</h2>
          <table className="w-full text-sm text-slate-900">
            <thead className="text-slate-500 uppercase text-xs">
              <tr>
                <th className="text-left py-2">Type</th>
                <th className="text-left py-2">Total</th>
                <th className="text-left py-2">With Disease</th>
                <th className="text-left py-2">Rate</th>
              </tr>
            </thead>
            <tbody>
              {thalStats.map(t => (
                <tr key={t.thal_type} className="border-t">
                  <td className="py-2">{t.thal_type}</td>
                  <td className="py-2">{t.total}</td>
                  <td className="py-2">{t.with_disease}</td>
                  <td className="py-2">{Math.round(t.with_disease / t.total * 100)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="bg-white rounded-lg shadow p-6 md:col-span-2">
          <h2 style={{color: '#0f172a'}} className="text-lg font-semibold mb-4">Risk Factors by Heart Disease Presence</h2>
          <table className="w-full text-sm text-slate-900">
            <thead className="text-slate-500 uppercase text-xs">
              <tr>
                <th className="text-left py-2">Heart Disease</th>
                <th className="text-left py-2">Avg Age</th>
                <th className="text-left py-2">Avg Cholesterol</th>
                <th className="text-left py-2">Avg Blood Pressure</th>
                <th className="text-left py-2">Avg Max Heart Rate</th>
              </tr>
            </thead>
            <tbody>
              {riskFactors.map(r => (
                <tr key={r.heart_disease_present} className="border-t">
                  <td className="py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      r.heart_disease_present > 0
                        ? 'bg-red-100 text-red-700'
                        : 'bg-green-100 text-green-700'
                    }`}>
                      {r.heart_disease_present > 0 ? 'Yes' : 'No'}
                    </span>
                  </td>
                  <td className="py-2">{r.avg_age}</td>
                  <td className="py-2">{r.avg_cholesterol}</td>
                  <td className="py-2">{r.avg_blood_pressure}</td>
                  <td className="py-2">{r.avg_max_heart_rate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Stats;