import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Accounts from "./pages/Accounts";
import Analytics from "./pages/Analytics";

function App() {

  return (
    <BrowserRouter>

      <div className="flex bg-slate-950 min-h-screen text-white">

        <Sidebar />

        <div className="ml-72 w-full">

          <Routes>

            <Route path="/" element={<Dashboard />} />

            <Route
              path="/transactions"
              element={<Transactions />}
            />

            <Route
              path="/accounts"
              element={<Accounts />}
            />

            <Route
              path="/analytics"
              element={<Analytics />}
            />

          </Routes>

        </div>

      </div>

    </BrowserRouter>
  );
}

export default App;