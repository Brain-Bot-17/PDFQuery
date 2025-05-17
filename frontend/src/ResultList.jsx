const ResultList = ({ results }) => {
  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">🧠 Top Matches</h3>
      <ul className="list-disc pl-5 space-y-2">
        {results.map((res, idx) => (
          <li key={idx} className="bg-gray-100 p-3 rounded">
            {res}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ResultList;
