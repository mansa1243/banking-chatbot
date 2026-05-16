function Transactions() {

  return (
    <div className="p-8">

      <h1 className="text-4xl font-bold mb-8">
        Transactions
      </h1>

      <div className="bg-slate-900 p-6 rounded-3xl">

        <div className="flex justify-between p-4 border-b border-slate-800">
          <span>Amazon</span>
          <span className="text-red-400">
            -₹2,000
          </span>
        </div>

        <div className="flex justify-between p-4 border-b border-slate-800">
          <span>Salary</span>
          <span className="text-green-400">
            +₹50,000
          </span>
        </div>

      </div>

    </div>
  );
}

export default Transactions;