import React from 'react'

const ExampleRepo = ({ setRepoUrl}) => {
  const exampleRepos = [
    { name: "VirtualAirHockey", path: "/anushika1206/virtual-air-hockey/main" },
    { name: "FastAPI", path: "/yourusername/fastapi/main" },
    { name: "Flask", path: "/yourusername/flask/main" },
    { name: "Excalidraw", path: "/yourusername/excalidraw/main" },
    { name: "ApiAnalytics", path: "/yourusername/api-analytics/main" }
  ];

  return (
    <div>
       <div className="mt-4">
      <p className="text-sm text-gray-400 mb-2">Example repositories:</p>
      <div className="flex flex-wrap gap-2">
        {exampleRepos.map((repo) => (
          <button
            key={repo.name}
            onClick={() => setRepoUrl(`https://github.com${repo.path}`)}
            className="px-3 py-1 bg-gray-800 rounded text-sm text-gray-300 hover:bg-gray-700"
          >
            {repo.name}
          </button>
        ))}
      </div>
    </div>
    </div>
  )
}

export default ExampleRepo