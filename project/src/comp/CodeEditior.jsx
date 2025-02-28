import React from 'react';
import { Code } from 'lucide-react';

const CodeEditor = ({ fileName, content }) => {
  return (
    <div className="flex-grow border-r border-[#21262d] flex flex-col bg-[#0d1117]/90 backdrop-blur-sm">
      <div className="p-3 border-b border-[#21262d] font-mono text-sm bg-[#161b22] flex items-center">
        <Code size={16} className="mr-2 text-[#58a6ff]" />
        {fileName}
      </div>
      <div className="flex-grow overflow-auto bg-[#0d1117]">
        <pre className="p-4 font-mono text-sm whitespace-pre-wrap text-[#e6edf3] leading-relaxed">
          <code>{content}</code>
        </pre>
      </div>
    </div>
  );
};

export default CodeEditor;