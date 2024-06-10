// app/api/hello/route.ts

import { NextResponse } from 'next/server';

export async function GET() {
  const vehicleLogsResponse = await fetch('https://c449-129-210-115-236.ngrok-free.app/vehicle-logs');
  const vehicleLogs = await vehicleLogsResponse.json();
  console.log("ASDASD"+vehicleLogs)
  return NextResponse.json({data:vehicleLogs});
}
