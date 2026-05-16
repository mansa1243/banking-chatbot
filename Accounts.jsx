function Accounts() {

  return (
    <div className="p-8">

      <h1 className="text-4xl font-bold mb-8">
        Accounts
      </h1>

      <div className="grid grid-cols-2 gap-6">

        <div className="bg-gradient-to-r from-cyan-500 to-blue-600 p-8 rounded-3xl">
          <h2 className="text-2xl">
            Savings Account
          </h2>

          <h1 className="text-5xl font-bold mt-6">
            ₹4,50,000
          </h1>
        </div>

        <div className="bg-gradient-to-r from-purple-500 to-pink-600 p-8 rounded-3xl">
          <h2 className="text-2xl">
            Credit Card
          </h2>

          <h1 className="text-5xl font-bold mt-6">
            ₹1,20,000
          </h1>
        </div>

      </div>

    </div>
  );
}

export default Accounts;