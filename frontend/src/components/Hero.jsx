import React from 'react'
import { Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'
import FloatingLogo from './FloatingLogo'

const Hero = () => {
  return (
    <div className="text-center relative">
      <motion.div 
        className="absolute -left-16 top-0"
        animate={{ 
          rotate: [12, -12, 12],
          scale: [1, 1.1, 1]
        }}
        transition={{ 
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        <Sparkles className="w-12 h-12 text-[#f85149]" />
      </motion.div>
      
      <motion.div 
        className="absolute -right-16 bottom-24"
        animate={{ 
          rotate: [-12, 12, -12],
          scale: [1, 1.1, 1]
        }}
        transition={{ 
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1.5
        }}
      >
        <Sparkles className="w-12 h-12 text-[#3fb950]" />
      </motion.div>
      
      <motion.h1 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.7 }}
        className="text-6xl font-bold mb-6 text-[#c9d1d9]"
      >
        Git the gist,<br />fast
      </motion.h1>

      <div className="h-32 my-12">
        <FloatingLogo />
      </div>
      
      <motion.p 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.7, delay: 0.2 }}
        className="text-xl text-[#8b949e] max-w-2xl mx-auto"
      >
        Turn any Git repository into a simple text digest of its codebase. This is useful for feeding a codebase into any LLM.
      </motion.p>
    </div>
  )
}

export default Hero