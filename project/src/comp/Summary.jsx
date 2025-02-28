import React from 'react';
import { ChevronRight } from 'lucide-react';

const Summary = ({ summary,fileName }) => {
  console.log(summary.summary["Filewise-Summary"]);
  return (
    <div className="h-1/2 border-b border-[#21262d] overflow-auto">
      <div className="p-3 border-b border-[#21262d] font-semibold flex items-center">
        <ChevronRight size={18} className="mr-2 text-[#58a6ff]" />
        Summary
      </div>
      <div className="p-4">
       
        <h2 className="text-lg text-white-400 font-bold mb-3">
          {fileName}
        </h2>
        <p className="text-m text-gray-400 mb-3">
          {summary.summary["Filewise-Summary"][fileName]}
        </p>
        
       {  !fileName &&<div className="space-y-2 text-sm">
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
        </div>}
      </div>
    </div>
  );
};

export default Summary;