import React, { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Float, Text3D, Center } from '@react-three/drei'
import { motion } from 'framer-motion-3d'

function FloatingText() {
  const textRef = useRef()

  useFrame((state) => {
    const t = state.clock.getElapsedTime()
    textRef.current.position.y = Math.sin(t) * 0.1
  })

  return (
    <Float
      speed={1.5}
      rotationIntensity={0.5}
      floatIntensity={0.5}
    >
      <Center ref={textRef}>
        <Text3D
          font="/fonts/Inter_Bold.json" // You'll need to provide this font
          size={0.5}
          height={0.1}
          curveSegments={12}
        >
          {`Git\ndeci`}
          <meshStandardMaterial color="#58a6ff" />
        </Text3D>
      </Center>
    </Float>
  )
}

const Hero3D = () => {
  return (
    <div className="h-40 w-full">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <FloatingText />
      </Canvas>
    </div>
  )
}

export default Hero3D 