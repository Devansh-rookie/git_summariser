import React, { useState } from 'react';
import { Maximize2, Minimize2, Download } from 'lucide-react';

const CardDatabox = ({ title, children, content }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const handleDownload = () => {
    // Get content to download - either from content prop or try to extract from children
    let downloadContent = '';
    
    if (content) {
      // If content prop is provided, use it
      downloadContent = typeof content === 'object' 
        ? JSON.stringify(content, null, 2) 
        : String(content);
    } else {
      // Try to extract content from children if it's a pre tag with JSON
      try {
        // This is a simple approach that works with our current implementation
        // where children is a pre tag with JSON content
        const childrenAsString = React.Children.toArray(children)
          .map(child => {
            if (React.isValidElement(child) && child.type === 'pre') {
              return child.props.children;
            }
            return '';
          })
          .join('');
        
        downloadContent = childrenAsString || 'No content available';
      } catch (error) {
        downloadContent = 'Error extracting content for download';
      }
    }

    // Create a blob and download link
    const blob = new Blob([downloadContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.replace(/\s+/g, '_').toLowerCase()}.txt`;
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
  };

  if (isExpanded) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
        <div className="bg-gray-900 border border-gray-700 rounded-lg w-[70%] h-[70%] overflow-auto">
          <div className="sticky top-0 bg-gray-800 p-3 flex justify-between items-center border-b border-gray-700">
            <h2 className="text-lg font-medium text-gray-200">{title}</h2>
            <div className="flex space-x-2">
              <button 
                onClick={handleDownload} 
                className="p-1 rounded-md hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
                aria-label="Download"
                title="Download as text file"
              >
                <Download size={18} />
              </button>
              <button 
                onClick={toggleExpand} 
                className="p-1 rounded-md hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
                aria-label="Minimize"
                title="Minimize"
              >
                <Minimize2 size={18} />
              </button>
            </div>
          </div>
          <div className="p-4 overflow-auto">
            {children}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-lg h-[300px] overflow-hidden">
      <div className="bg-gray-800 p-3 flex justify-between items-center border-b border-gray-700">
        <h2 className="text-lg font-medium text-gray-200">{title}</h2>
        <div className="flex space-x-2">
          <button 
            onClick={handleDownload} 
            className="p-1 rounded-md hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
            aria-label="Download"
            title="Download as text file"
          >
            <Download size={18} />
          </button>
          <button 
            onClick={toggleExpand} 
            className="p-1 rounded-md hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
            aria-label="Expand"
            title="Expand"
          >
            <Maximize2 size={18} />
          </button>
        </div>
      </div>
      <div className="p-4 overflow-auto h-[calc(300px-56px)]">
        {children}
      </div>
    </div>
  );
};

export default CardDatabox;