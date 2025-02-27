import React, { useState, useEffect, Suspense } from "react";
import {Sparkles,Copy,Check,Github,Code2,FileJson,FileCode, FileText,Package,GitBranch,RefreshCw,
} from "lucide-react";
import Footer from "./components/footer";
import DataBox from "./components/Databox";
import ExampleRepo from "./components/ExampleRepo";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Button from "./components/button";
import Particles from "./components/Particles";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [projec, setProjec] = useState(false);
  const [data, setData] = useState({});

  const extractRepoData = (url) => {
    if (url.startsWith("https://github.com/")) {
      const data1 = url.split(".com/")[1].split("/");
      const data2 = {
        "owner": data1[0],
        "repo": data1[1],
        "branch": data1[2] || "main" // Default to "main" if branch is not specified
      };
      return data2;
    }
    return null; // Return null if the URL is not valid
  };

  const generateMessage = async () => {
    const repoData = extractRepoData(repoUrl); // Extract data when button is clicked
    if (repoData) {
      setLoading(true);
      setProjec(true);
      setData(repoData);
      try {
        const response = await fetch(`http://localhost:8002/api/fetch/?owner=${repoData.owner}&repo=${repoData.repo}&branch=${repoData.branch}`);
        if (!response.ok) throw new Error('Failed to fetch data');
        const result = await response.json();
        setData(result); 
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    } else {
      alert("Please enter a valid GitHub repository URL");
    }
  };

  return (
    <div className="min-h-screen text-white">
      <Suspense fallback={null}>
        <Particles />
      </Suspense>

      <div className="relative z-10">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <Header />

          <main className="mt-24 max-w-3xl mx-auto">
            <Hero />

            <div className="mt-12">
              <div className="bg-[#161b22]/80 border border-[#30363d] rounded-xl p-8 backdrop-blur-sm">
                <div>
                  <input
                    type="text"
                    value={repoUrl}
                    onChange={(e) => setRepoUrl(e.target.value)}
                    
                    
                    placeholder="https://github.com/"
                    className="w-full px-4 py-3 bg-[#0d1117]/50 border border-[#30363d] rounded-lg focus:ring-2 focus:ring-[#58a6ff] focus:border-[#58a6ff] transition-all text-[#c9d1d9] placeholder-[#8b949e]"
                  />
                </div>

                <div className="mt-4">
                  <button
                    onClick={generateMessage}
                    className="w-full bg-gradient-to-r from-[#238636] to-[#2ea043] text-[#ffffff] font-medium py-3 px-6 rounded-lg transition-all hover:from-[#2ea043] hover:to-[#3fb950] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-[#238636] flex items-center justify-center gap-2 shadow-lg hover:shadow-xl"
                  >
                    Do Magic
                  </button>
                </div>

                <div className="mt-6">
                  <ExampleRepo setRepoUrl={setRepoUrl} />
                </div>
                {projec && (
                  <div className="mt-8">
                    <DataBox 
                      owner={data.owner}
                      repo={data.repo}
                      branch={data.branch}
                      repoUrl={repoUrl}
                    />
                  </div>
                )}
              </div>
            </div>
          </main>

          <Footer />
        </div>
      </div>
    </div>
  );
}

export default App;
