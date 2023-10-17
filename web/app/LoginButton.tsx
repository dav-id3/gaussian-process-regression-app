"use client"

import { signIn } from "next-auth/react"
export const LoginButton = () => {
  return (
    <>
      Not signed in <br />
      <button onClick={() => signIn()}>Sign in</button>
    </>
  )
}
