import React from 'react';
import { FileText, Code } from 'lucide-react';

const FileExplorer = ({ files, selectedFile, onSelectFile }) => {
  return (
    <div className="w-64 border-r border-[#21262d] flex flex-col bg-[#0d1117]/80 backdrop-blur-sm">
      <div className="p-4 border-b border-[#21262d] font-semibold flex items-center">
        <FileText size={18} className="mr-2 text-[#58a6ff]" />
        Files
      </div>
      <div className="overflow-y-auto flex-grow">
        {files.map(({ name, content }) => (
          <div 
            key={name}
            className={`p-3 flex items-center cursor-pointer transition-colors duration-200 hover:bg-[#161b22] ${selectedFile.name === name ? 'bg-[#161b22] border-l-2 border-[#58a6ff]' : ''}`}
            onClick={() => onSelectFile({ name, content })}
          >
            <Code size={16} className="mr-2 text-[#58a6ff]" />
            {name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FileExplorer;