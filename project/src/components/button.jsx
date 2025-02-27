import React from "react";
import { Sparkles } from 'lucide-react'

const Button = ({ repoUrl, loading, generateMessage }) => {
  return (
    <div>
      <button
        onClick={generateMessage}
        disabled={!repoUrl.trim() || loading}
        className="w-full bg-gradient-to-r from-[#238636] to-[#2ea043] text-[#ffffff] font-medium py-3 px-6 rounded-lg transition-all hover:from-[#2ea043] hover:to-[#3fb950] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-[#238636] flex items-center justify-center gap-2 shadow-lg hover:shadow-xl"
      >
        {loading ? (
          <div className="rounded-full h-5 w-5 border-2 border-white border-t-transparent animate-spin" />
        ) : (
          <Sparkles className="w-5 h-5" />
        )}
        <span className="relative">
          Do Magic
          {!loading && (
            <span className="absolute bottom-0 left-0 w-full h-0.5 bg-white/30" />
          )}
        </span>
      </button>
    </div>
  );
};

export default Button;
