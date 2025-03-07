import React, { useState } from 'react';
import useMultiFetch from './useMultiFetch';
import { useGithubRepoData } from './useGithubrepo';
import CardDatabox from './CardDatabox';
import SearchBox from './SearchBox';
const backend_url = import.meta.env.VITE_BACKEND_URL;
const Databox = ({ owner, repo, branch,repoUrl }) => {
  const [shouldFetch] = useState({
    summary: `${backend_url}/api/summary/?owner=${owner}&repo=${repo}&branch=${branch}`,
    dependencies: `${backend_url}/api/fetch/?owner=${owner}&repo=${repo}&branch=${branch}`,
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
          <CardDatabox key={key} title={value.type} content={value.data}>
          <p className="text-sm text-gray-400" 
            dangerouslySetInnerHTML={{ 
              __html: JSON.stringify(value.data, null, 2).replace(/\\n/g, '<br />') 
            }} 
         />
       </CardDatabox>
        ))}
        {Object.entries(data.summary["summary"] || {}).map(([key, value]) => (
          <CardDatabox key={key} title={key} content={value}>
          <p className="text-sm text-gray-400" 
            dangerouslySetInnerHTML={{ 
              __html: JSON.stringify(value, null, 2).replace(/\\n/g, '<br />') 
            }} 
         />
       </CardDatabox>
        ))}
        <SearchBox owner={owner} repo={repo} branch={branch} />
      </div>
    </>
  );
}

export default Databox;