// app/api/hello/route.ts

import { NextResponse } from 'next/server';

export async function GET() {
  const trafficStatsResponse = await fetch('https://fb6c-2601-647-4d83-3930-00-da51.ngrok-free.app/traffic-stats');
  const trafficStats = await trafficStatsResponse.json();
  console.log(trafficStats)
  return NextResponse.json({data:trafficStats});
}
