import React, { useState } from 'react'
import CardDatabox from './CardDatabox'
import { Search } from 'lucide-react'

const SearchBox = ({ owner, repo, branch }) => {
    const [search, setSearch] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchSearchResults = async () => {
        if (!search) return;

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`http://localhost:8002/api/search/?owner=${owner}&repo=${repo}&branch=${branch}&query=${search}`);
            if (!response.ok) throw new Error('Failed to fetch search results');

            const data = await response.json();
            console.log("API Response:", data);

            // Convert the object to an array of results
            const resultsArray = Object.entries(data).map(([filename, content]) => ({
                filename,
                content,
            }));

            // Check if resultsArray is not empty
            if (resultsArray.length > 0) {
                setSearchResults(resultsArray);
            } else {
                throw new Error('No results found');
            }
        } catch (err) {
            console.error("Error fetching search results:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="flex items-center gap-2">
            <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search..."
                className="w-full px-4 py-3 bg-[#0d1117]/50 border border-[#30363d] rounded-lg focus:ring-2 focus:ring-[#58a6ff] focus:border-[#58a6ff] transition-all text-[#c9d1d9] placeholder-[#8b949e]"
            />
            <button 
                className="text-white hover:text-gray-400 cursor-pointer font-semibold transition-colors border-[#58a6ff] border-2 rounded-md px-4 py-2" 
                onClick={fetchSearchResults}
            >
                Search
            </button>
            </div>
            {loading && <div>Loading...</div>}
            {error && <div className="mt-4"> <CardDatabox 
                        title="Search Results"
                        content={null}
                    >
                        <pre className="text-sm text-gray-400">{JSON.stringify(null, null, 2)}</pre>
                    </CardDatabox></div>}
            <div className="mt-4">
                {!error && <CardDatabox 
                        title="Search Results"
                        content={searchResults}
                    >
                        <pre className="text-sm text-gray-400">{JSON.stringify(searchResults, null, 2)}</pre>
                    </CardDatabox>}
            </div>
        </div>
    )
}

export default SearchBox