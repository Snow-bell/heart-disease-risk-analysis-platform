import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import Stats from './pages/Stats';
import Predict from './pages/Predict';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/patients" element={<Patients />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/predict" element={<Predict />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;