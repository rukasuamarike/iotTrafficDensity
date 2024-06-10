// app/api/hello/route.ts

import { NextResponse } from 'next/server';

export async function GET() {
  const trafficStatsResponse = await fetch('https://c449-129-210-115-236.ngrok-free.app/traffic-stats');
  const trafficStats = await trafficStatsResponse.json();
  console.log(trafficStats)
  return NextResponse.json({data:trafficStats});
}
