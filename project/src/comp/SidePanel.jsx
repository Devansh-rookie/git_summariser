import React from 'react';
import Summary from './Summary';
import ChatSection from './ChatSection';

const SidePanel = ({ selectedFileName, initialMessages }) => {
  return (
    <div className="w-96 flex flex-col bg-[#0d1117]/80 backdrop-blur-sm">
      <Summary fileName={selectedFileName} />
      <ChatSection initialMessages={initialMessages} selectedFileName={selectedFileName} />
    </div>
  );
};

export default SidePanel;