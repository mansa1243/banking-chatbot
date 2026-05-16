import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import StatsCard from "../components/StatsCard";
import AnalyticsChart from "../components/AnalyticsChart";
import TransactionList from "../components/TransactionList";
import AIChat from "../components/AIChat";

function Dashboard() {

  return (
    <div className="flex bg-slate-950 min-h-screen">

      <Sidebar />

      <div className="ml-72 w-full p-8">

        <Navbar />

        <div className="grid grid-cols-4 gap-6 mb-8">

          <StatsCard
            title="Balance"
            value="₹4,50,000"
            gradient="bg-gradient-to-r from-cyan-500 to-blue-600"
          />

          <StatsCard
            title="Savings"
            value="₹2,40,000"
            gradient="bg-gradient-to-r from-green-500 to-emerald-600"
          />

          <StatsCard
            title="Transactions"
            value="128"
            gradient="bg-gradient-to-r from-purple-500 to-pink-600"
          />

          <StatsCard
            title="AI Score"
            value="98%"
            gradient="bg-gradient-to-r from-orange-500 to-red-600"
          />

        </div>

        <div className="grid grid-cols-3 gap-6 mb-8">

          <div className="col-span-2">
            <AnalyticsChart />
          </div>

          <AIChat />

        </div>

        <TransactionList />

      </div>

    </div>
  );
}

export default Dashboard;