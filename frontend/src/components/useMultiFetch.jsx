import { useState, useEffect } from "react";

const useMultiFetch = (urlMap) => {
  const [data, setData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const entries = Object.entries(urlMap); 

        const results = await Promise.all(
          entries.map(async ([key, url]) => {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to fetch ${key} from ${url}`);

            const contentType = response.headers.get("content-type");
            const result = contentType.includes("application/json")
              ? await response.json()
              : await response.text();

            return { [key]: result };
          })
        );
        const mergedData = Object.assign({}, ...results);
        setData(mergedData);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [urlMap]);

  return { data, isLoading, error };
};

export default useMultiFetch;