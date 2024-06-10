"use client"
import Image from "next/image";
import React, { useState, useEffect } from 'react';

import Dashboard from '../components/dashboard';

export default function Home() {

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      
      <Dashboard></Dashboard>
      
     
    </main>
  );
}
