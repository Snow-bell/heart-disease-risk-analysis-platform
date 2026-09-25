import { useEffect, useState } from 'react';
import client from '../api/client';

interface Patient {
  patient_id: number;
  age: number;
  sex: number;
  cp: string;
  trestbps: number;
  chol: number;
  fbs: number;
  restecg: string;
  thalach: number;
  exang: number;
  oldpeak: number;
  slope: string;
  ca: number;
  thal: string;
  heart_disease_present: number;
}

function Patients() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [sexFilter, setSexFilter] = useState('');
  const [hdFilter, setHdFilter] = useState('');

  useEffect(() => {
    const params: Record<string, string> = {};
    if (sexFilter !== '') params.sex = sexFilter;
    if (hdFilter !== '') params.heart_disease_present = hdFilter;

    client.get('/api/patients/', { params })
      .then(res => setPatients(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [sexFilter, hdFilter]);

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold text-blue-900 mb-6">Patients</h1>

      <div className="flex gap-4 mb-6">
        <select
          className="border rounded px-3 py-2 text-sm"
          value={sexFilter}
          onChange={e => setSexFilter(e.target.value)}
        >
          <option value="">All Sexes</option>
          <option value="1">Male</option>
          <option value="0">Female</option>
        </select>

        <select
          className="border rounded px-3 py-2 text-sm"
          value={hdFilter}
          onChange={e => setHdFilter(e.target.value)}
        >
          <option value="">All Patients</option>
          <option value="1">Heart Disease Present</option>
          <option value="0">No Heart Disease</option>
        </select>
      </div>

      <div className="bg-white rounded-lg shadow overflow-x-auto">
        <table className="w-full text-sm text-left text-slate-900">
          <thead className="bg-gray-300 text-slate-900 uppercase text-xs">
            <tr>
              <th className="px-4 py-3">ID</th>
              <th className="px-4 py-3">Age</th>
              <th className="px-4 py-3">Sex</th>
              <th className="px-4 py-3">Chest Pain</th>
              <th className="px-4 py-3">BP</th>
              <th className="px-4 py-3">Cholesterol</th>
              <th className="px-4 py-3">Thalach</th>
              <th className="px-4 py-3">Thal</th>
              <th className="px-4 py-3">Heart Disease</th>
            </tr>
          </thead>
          <tbody>
            {patients.map(p => (
              <tr key={p.patient_id} className="border-t hover:bg-slate-50">
                <td className="px-4 py-3">{p.patient_id}</td>
                <td className="px-4 py-3">{p.age}</td>
                <td className="px-4 py-3">{p.sex === 1 ? 'Male' : 'Female'}</td>
                <td className="px-4 py-3">{p.cp}</td>
                <td className="px-4 py-3">{p.trestbps}</td>
                <td className="px-4 py-3">{p.chol}</td>
                <td className="px-4 py-3">{p.thalach}</td>
                <td className="px-4 py-3">{p.thal}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    p.heart_disease_present > 0
                      ? 'bg-red-100 text-red-700'
                      : 'bg-green-100 text-green-700'
                  }`}>
                    {p.heart_disease_present > 0 ? 'Yes' : 'No'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Patients;