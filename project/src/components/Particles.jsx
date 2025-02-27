import React, { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Points, PointMaterial } from '@react-three/drei'
import * as THREE from 'three'

function ParticleField() {
  const ref = useRef()
  
  const count = 3000
  const radius = 12
  
  const positions = useMemo(() => {
    const positions = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)
    const color = new THREE.Color()
    
    for (let i = 0; i < count; i++) {
      const theta = THREE.MathUtils.randFloatSpread(360)
      const phi = THREE.MathUtils.randFloatSpread(360)
      
      positions[i * 3] = radius * Math.sin(theta) * Math.cos(phi)
      positions[i * 3 + 1] = radius * Math.sin(theta) * Math.sin(phi)
      positions[i * 3 + 2] = radius * Math.cos(theta)

      color.setHSL(0.5 + Math.random() * 0.1, 0.8, 0.6)
      colors[i * 3] = color.r
      colors[i * 3 + 1] = color.g
      colors[i * 3 + 2] = color.b
    }
    return { positions, colors }
  }, [count])

  useFrame((state) => {
    const time = state.clock.getElapsedTime()
    ref.current.rotation.x = Math.sin(time / 10) * 0.1
    ref.current.rotation.y = Math.cos(time / 15) * 0.1
    ref.current.rotation.z = Math.sin(time / 20) * 0.1

    const { x, y } = state.mouse
    ref.current.rotation.x += x * 0.1
    ref.current.rotation.y += y * 0.1
  })

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={positions.positions} colors={positions.colors} stride={3} frustumCulled={false}>
        <PointMaterial
          transparent
          vertexColors
          size={0.03}
          sizeAttenuation={true}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </Points>
    </group>
  )
}

function MovingGradient() {
  const mesh = useRef()
  
  useFrame((state) => {
    const time = state.clock.getElapsedTime()
    mesh.current.position.y = Math.sin(time / 2) * 0.3
    mesh.current.rotation.z = Math.sin(time / 4) * 0.2
    
    const { x, y } = state.mouse
    mesh.current.position.x = x * 0.1
    mesh.current.position.y += y * 0.1
  })

  return (
    <mesh ref={mesh} position={[0, 0, -5]} scale={[15, 15, 1]}>
      <planeGeometry />
      <meshBasicMaterial
        color="#0d1117"
        opacity={0.8}
        transparent
        blending={THREE.AdditiveBlending}
      />
    </mesh>
  )
}

export default function Particles() {
  return (
    <div className="fixed top-0 left-0 w-full h-full -z-10">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 75 }}
        style={{ background: '#0d1117' }}
      >
        <MovingGradient />
        <ParticleField />
      </Canvas>
    </div>
  )
} 