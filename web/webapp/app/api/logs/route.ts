
import { NextResponse } from 'next/server';

export async function GET() {
  const vehicleLogsResponse = await fetch('https://fb6c-2601-647-4d83-3930-00-da51.ngrok-free.app/vehicle-logs',{ cache: 'no-store' });
  const vehicleLogs = await vehicleLogsResponse.json();
  console.log("ASDASD"+vehicleLogs)
  return NextResponse.json({data:vehicleLogs});
}
