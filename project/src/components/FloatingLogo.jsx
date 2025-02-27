import React, { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Float, MeshDistortMaterial } from '@react-three/drei'

function Logo() {
  const ref = useRef()
  const sphereRef = useRef()

  useFrame((state) => {
    const time = state.clock.getElapsedTime()
    ref.current.rotation.x = Math.cos(time / 4) * 0.2
    ref.current.rotation.y = Math.sin(time / 4) * 0.2
    
    // Mouse interaction
    const { x, y } = state.mouse
    ref.current.rotation.x += x * 0.1
    ref.current.rotation.y += y * 0.1
    
    // Pulse effect
    sphereRef.current.scale.x = 1 + Math.sin(time * 2) * 0.05
    sphereRef.current.scale.y = 1 + Math.sin(time * 2) * 0.05
    sphereRef.current.scale.z = 1 + Math.sin(time * 2) * 0.05
  })

  return (
    <Float
      speed={2} 
      rotationIntensity={0.5} 
      floatIntensity={0.5}
    >
      <group ref={ref}>
        {/* Main sphere */}
        <mesh ref={sphereRef}>
          <sphereGeometry args={[0.6, 64, 64]} />
          <MeshDistortMaterial
            color="#58a6ff"
            envMapIntensity={0.4}
            clearcoat={0.8}
            clearcoatRoughness={0}
            metalness={0.2}
            roughness={0.1}
            distort={0.4}
            speed={2}
          />
        </mesh>

        {/* Orbiting rings */}
        <mesh rotation-x={Math.PI / 2}>
          <torusGeometry args={[0.8, 0.02, 16, 100]} />
          <meshStandardMaterial color="#58a6ff" emissive="#58a6ff" emissiveIntensity={0.5} />
        </mesh>
        <mesh rotation-x={Math.PI / 3} rotation-y={Math.PI / 6}>
          <torusGeometry args={[0.9, 0.02, 16, 100]} />
          <meshStandardMaterial color="#58a6ff" emissive="#58a6ff" emissiveIntensity={0.5} />
        </mesh>
      </group>
    </Float>
  )
}

export default function FloatingLogo() {
  return (
    <div className="h-40 w-full cursor-pointer">
      <Canvas camera={{ position: [0, 0, 2.5] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        <Logo />
      </Canvas>
    </div>
  )
} 