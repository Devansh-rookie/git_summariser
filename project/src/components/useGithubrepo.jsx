import { useState, useEffect } from "react";

const useGithubRepoData = (repoUrl, summaryUrl, dependencyUrl) => {
  const [data, setData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        console.log("Fetching data from:", summaryUrl, dependencyUrl);
        
        // Log the URLs to ensure they are correct
        if (!summaryUrl || !dependencyUrl) {
          throw new Error("Summary URL or Dependency URL is undefined");
        }

        const [summaryRes, dependencyRes] = await Promise.all([
          fetch(summaryUrl).then((res) => {
            if (!res.ok) throw new Error('Failed to fetch summary');
            return res.json();
          }),
          fetch(dependencyUrl).then((res) => {
            if (!res.ok) throw new Error('Failed to fetch dependencies');
            return res.json();
          }),
        ]);
        
        setData({ summary: summaryRes, dependencies: dependencyRes });
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    if (summaryUrl && dependencyUrl) {
      fetchData();
    }
  }, [summaryUrl, dependencyUrl]);

  return { data, isLoading, error };
};

export default useGithubRepoData;
