import React, { useState } from 'react';
import useMultiFetch from './useMultiFetch';
import { useGithubRepoData } from './useGithubrepo';

const Databox = ({ owner, repo, branch,repoUrl }) => {
  const [shouldFetch] = useState({
    summary: `http://localhost:8002/api/summary/?owner=${owner}&repo=${repo}&branch=${branch}`,
    dependencies: `http://localhost:8002/api/fetch/?owner=${owner}&repo=${repo}&branch=${branch}`,
  });

  // Fetch data using the hook
  const { data, isLoading, error } = useGithubRepoData(repoUrl, shouldFetch.summary, shouldFetch.dependencies);
  localStorage.setItem("data", JSON.stringify(data));
  if (error) return <div>Error: {error}</div>;
  if (isLoading) return <div>Loading...</div>;

  return (
    <>
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(data.dependencies["data"] || {}).map(([key, value]) => (
          <div key={key} className="bg-gray-900 border border-gray-700 rounded-lg p-4">
            <h1 className="text-lg text-gray-200 mb-2">{value.type}</h1>
            <p className="text-sm text-gray-400" 
               dangerouslySetInnerHTML={{ 
                 __html: JSON.stringify(value.data, null, 2).replace(/\\n/g, '<br />') 
               }} 
            />
          </div>
        ))}
        {Object.entries(data.summary["summary"] || {}).map(([key, value]) => (
          <div key={key} className="bg-gray-900 border border-gray-700 rounded-lg p-4">
            <h1 className="text-lg text-gray-200 mb-2">{key}</h1>
            <p className="text-sm text-gray-400" 
               dangerouslySetInnerHTML={{ 
                 __html: JSON.stringify(value, null, 2).replace(/\\n/g, '<br />') 
               }} 
            />
          </div>
        ))}
      </div>
    </>
  );
}

export default Databox;