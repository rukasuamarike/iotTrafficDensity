"use client"
import Image from "next/image";
import React, { useState, useEffect } from 'react';

import Dashboard from '../components/dashboard';

export default function Home() {
  useEffect(() => {
    
    const fetchData = async () => {
      const response = await fetch('/api/hello');
      const data = await response.json();
      console.log(data);
      // setMessage(data.message);
    };
    fetchData();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      
      <Dashboard></Dashboard>
      
     
    </main>
  );
}
