import { Github, Instagram, Mail } from 'lucide-react'
import { motion } from 'framer-motion'

const Footer = () => {
  return (
    <motion.footer 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="mt-16 text-[#8b949e] text-sm"
    >
      <div className="flex justify-between items-center max-w-4xl mx-auto">
        <div className="flex items-center gap-4">
          <motion.a 
            whileHover={{ scale: 1.1, rotate: 10 }}
            whileTap={{ scale: 0.9 }}
            href="https://github.com/Devansh-rookie/git_summariser" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="hover:text-[#c9d1d9] transition-colors"
          >
            <Github className="w-5 h-5" />
          </motion.a>
          <motion.a 
            whileHover={{ scale: 1.1, rotate: -10 }}
            whileTap={{ scale: 0.9 }}
            href="mailto:123110029@nitkkr.ac.in" 
            className="hover:text-[#c9d1d9] transition-colors"
          >
            <Mail className="w-5 h-5" />
          </motion.a>
        </div>
        
        <div className="flex items-center gap-4">
          {['ch_rishabh2', 'devansh151005', 'pura.npalsingh', 'sanskaraggarwal720'].map((dev, index) => (
            <motion.a 
              key={index}
              whileHover={{ scale: 1.1, rotate: 10 }}
              whileTap={{ scale: 0.9 }}
              href={`https://instagram.com/${dev}`} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="hover:text-[#c9d1d9] transition-colors"
            >
              <Instagram className="w-5 h-5" />
            </motion.a>
          ))}
        </div>
      </div>
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
        className="mt-16 text-center text-[#8b949e] text-sm"
      >
        <p>Built with ❤️ to get better understanding of codebases</p>
      </motion.div>
    </motion.footer>
  )
}

export default Footer