import React from 'react';
import { Code, GitBranch, Star, GitPullRequest, Moon, Settings } from 'lucide-react';

const Header = () => {
  return (
    <div className="absolute top-0 left-0 right-0 h-12 bg-[#0d1117]/90 backdrop-blur-sm border-b border-[#21262d] flex items-center px-4 z-10">
      <div className="flex items-center text-[#58a6ff] font-semibold">
        <Code size={20} className="mr-2" />
        <span>Gitdeci</span>
      </div>
      <div className="ml-auto flex items-center space-x-4">
        <GitBranch size={18} className="text-gray-400 hover:text-gray-200 cursor-pointer transition-colors" />
        <Star size={18} className="text-gray-400 hover:text-gray-200 cursor-pointer transition-colors" />
        <GitPullRequest size={18} className="text-gray-400 hover:text-gray-200 cursor-pointer transition-colors" />
        <Moon size={18} className="text-gray-400 hover:text-gray-200 cursor-pointer transition-colors" />
        <Settings size={18} className="text-gray-400 hover:text-gray-200 cursor-pointer transition-colors" />
      </div>
    </div>
  );
};

export default Header;