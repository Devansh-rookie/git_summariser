import React from 'react';

const BackgroundEffects = () => {
  return (
    <>
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#0d1117] via-[#161b22] to-[#0d1117] opacity-80"></div>
      
      {/* Subtle animated glow effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-10 left-20 w-40 h-40 bg-[#58a6ff] rounded-full opacity-5 blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-60 h-60 bg-[#238636] rounded-full opacity-5 blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        <div className="absolute top-1/3 right-1/4 w-32 h-32 bg-[#ff5d5b] rounded-full opacity-5 blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
      </div>
    </>
  );
};

export default BackgroundEffects;