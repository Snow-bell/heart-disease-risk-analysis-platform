import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-slate-700 text-white px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <span className="text-lg font-semibold">Heart Disease Risk Analysis</span>
        <div className="flex gap-6">
          <Link to="/" className="hover:text-blue-400 transition-colors">Dashboard</Link>
          <Link to="/patients" className="hover:text-blue-400 transition-colors">Patients</Link>
          <Link to="/stats" className="hover:text-blue-400 transition-colors">Statistics</Link>
          <Link to="/predict" className="hover:text-blue-400 transition-colors">Risk Prediction</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;