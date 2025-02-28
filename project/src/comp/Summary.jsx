import React from 'react';
import { ChevronRight } from 'lucide-react';

const Summary = ({ fileName }) => {
  return (
    <div className="h-1/2 border-b border-[#21262d] overflow-auto">
      <div className="p-3 border-b border-[#21262d] font-semibold flex items-center">
        <ChevronRight size={18} className="mr-2 text-[#58a6ff]" />
        Summary
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2 text-[#e6edf3]">File Analysis</h3>
        <p className="text-sm text-gray-400 mb-3">
          {fileName} - React Component
        </p>
        <div className="space-y-2 text-sm">
          <div className="p-2 bg-[#161b22] rounded-md border border-[#30363d] hover:border-[#58a6ff]/50 transition-colors">
            <span className="text-[#58a6ff] font-semibold">Imports:</span> React, useState
          </div>
          <div className="p-2 bg-[#161b22] rounded-md border border-[#30363d] hover:border-[#58a6ff]/50 transition-colors">
            <span className="text-[#58a6ff] font-semibold">Component:</span> ExampleComponent
          </div>
          <div className="p-2 bg-[#161b22] rounded-md border border-[#30363d] hover:border-[#58a6ff]/50 transition-colors">
            <span className="text-[#58a6ff] font-semibold">State:</span> count (number)
          </div>
          <div className="p-2 bg-[#161b22] rounded-md border border-[#30363d] hover:border-[#58a6ff]/50 transition-colors">
            <span className="text-[#58a6ff] font-semibold">Actions:</span> Increment button
          </div>
        </div>
      </div>
    </div>
  );
};

export default Summary;