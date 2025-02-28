import React from 'react'
import { Code2, Github } from 'lucide-react'

const Header = () => {
  return (
    <nav className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Code2 className="w-6 h-6 text-[#c9d1d9]" />
        <span className="text-xl font-bold text-[#c9d1d9]">
          Git<span className="text-[#58a6ff]">deci</span>
        </span>
      </div>
      
      
      <a
        href="https://github.com"
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center gap-2 text-[#8b949e] hover:text-[#c9d1d9] transition-colors"
      >
        <Github className="w-5 h-5" />
        <span>GitHub</span>
      </a>
    </nav>
  )
}

export default Header