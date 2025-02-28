import React, { useState } from 'react';
import Header from './comp/Header';
import FileExplorer from './comp/FileExplorer';
import CodeEditor2 from './comp/CodeEditior';
import SidePanel from './comp/SidePanel';
import BackgroundEffects from './comp/BackgroundEffects';


function CodeEditor() {
  const [selectedFile, setSelectedFile] = useState({
  });

  const data = JSON.parse(localStorage.getItem('data'));
  // console.log(data);
  const { summary, dependencies } = data;



  const initialChatMessages = [
    { role: 'assistant', content: 'Hello! How can I help you with your code today?' },
  ];

  const filesObject = dependencies.data[0].data;
  console.log(filesObject);

  // Transforming the files object into an array of objects
  const filesArray = Object.entries(filesObject).map(([fileName, content]) => ({
    name: fileName,
    content: content,
  }));
  console.log(filesArray);

  return (
    <div className="flex h-screen bg-[#0a0c10] text-gray-200 overflow-hidden relative">
      <BackgroundEffects />
      <Header />

      {/* Main content - pushed down to account for header */}
      <div className="flex w-full mt-12 relative z-0">
        <FileExplorer 
          files={filesArray} 
          selectedFile={selectedFile} 
          onSelectFile={setSelectedFile} 
        />
        <CodeEditor2
          fileName={selectedFile.name} 
          content={selectedFile.content} 
        />
        <SidePanel 
          selectedFileName={selectedFile.name} 
          initialMessages={initialChatMessages} 
        />
      </div>
    </div>
  );
}

export default CodeEditor;