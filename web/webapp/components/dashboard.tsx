/**
* This code was generated by v0 by Vercel.
* @see https://v0.dev/t/hzz6w5ozQVB
* Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
*/

/** Add fonts into your Next.js project:

import { Inter } from 'next/font/google'

inter({
  subsets: ['latin'],
  display: 'swap',
})

To read more about using these font, please visit the Next.js documentation:
- App Directory: https://nextjs.org/docs/app/building-your-application/optimizing/fonts
- Pages Directory: https://nextjs.org/docs/pages/building-your-application/optimizing/fonts
**/
"use client"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { CardTitle, CardDescription, CardHeader, CardContent, Card } from "@/components/ui/card"
import { ResponsiveLine } from "@nivo/line"
import { TableHead, TableRow, TableHeader, TableCell, TableBody, Table } from "@/components/ui/table"

export default function Dashboard() {
  return (
    <div className="flex flex-col w-full min-h-screen bg-gray-100 dark:bg-gray-950">
      <header className="flex items-center h-16 px-6 border-b border-gray-200 dark:border-gray-800 shrink-0">
        <nav className="flex items-center gap-6 text-lg font-medium md:gap-8">
          <Link className="flex items-center gap-2 text-lg font-semibold" href="#">
            <Package2Icon className="w-6 h-6" />
            <span className="sr-only">Traffic Dashboard</span>
          </Link>
          <Link className="text-gray-500 dark:text-gray-400" href="#">
            Locations
          </Link>
          <Link className="text-gray-500 dark:text-gray-400" href="#">
            Vehicles
          </Link>
          <Link className="text-gray-500 dark:text-gray-400" href="#">
            Analytics
          </Link>
        </nav>
        <div className="ml-auto flex items-center gap-4">
          <Button className="rounded-full" size="icon" variant="ghost">
            <SearchIcon className="w-5 h-5 text-gray-500 dark:text-gray-400" />
            <span className="sr-only">Search</span>
          </Button>
          <Button className="rounded-full" size="icon" variant="ghost">
            <BellIcon className="w-5 h-5 text-gray-500 dark:text-gray-400" />
            <span className="sr-only">Notifications</span>
          </Button>
          <Button className="rounded-full" size="icon" variant="ghost">
            <img
              alt="Avatar"
              className="rounded-full"
              height="32"
              src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAADuWHzQAAAABGdBTUEAALGPC+tsAAAACSRlTUQAACAvQJRIiinnAAAAAAlwGQAAACxI4SlNBSYyIAAAACXBAJVACQAAAABhIJIPVQAAAABYBJybhwAAAABCA+FOiAECAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAAASUVORK5CYII="
              style={{
                aspectRatio: "32/32",
                objectFit: "cover",
              }}
              width="32"
            />
            <span className="sr-only">User menu</span>
          </Button>
        </div>
      </header>
      <main className="flex-1 grid gap-6 p-6 md:p-10">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Traffic Volume</CardTitle>
              <CardDescription>Trends over time</CardDescription>
            </CardHeader>
            <CardContent>
              <LineChart className="aspect-[4/3]" />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Average Speed</CardTitle>
              <CardDescription>Across all locations</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-5xl font-bold">45 mph</div>
              <div className="text-sm text-gray-500 dark:text-gray-400">+2.3% from last week</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Congestion Level</CardTitle>
              <CardDescription>Current status</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-5xl font-bold">62%</div>
              <div className="text-sm text-gray-500 dark:text-gray-400">-4.1% from last week</div>
            </CardContent>
          </Card>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Traffic Predictions</CardTitle>
              <CardDescription>Next 24 hours</CardDescription>
            </CardHeader>
            <CardContent>
              <LineChart className="aspect-[4/3]" />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Vehicle Logs</CardTitle>
              <CardDescription>Recent detections</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Time</TableHead>
                    <TableHead>Location</TableHead>
                    <TableHead>Vehicle</TableHead>
                    <TableHead>Speed</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell>2:45 PM</TableCell>
                    <TableCell>Main St</TableCell>
                    <TableCell>Sedan</TableCell>
                    <TableCell>42 mph</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>2:41 PM</TableCell>
                    <TableCell>Elm Rd</TableCell>
                    <TableCell>SUV</TableCell>
                    <TableCell>38 mph</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>2:37 PM</TableCell>
                    <TableCell>Oak Ave</TableCell>
                    <TableCell>Truck</TableCell>
                    <TableCell>35 mph</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>2:33 PM</TableCell>
                    <TableCell>Park Blvd</TableCell>
                    <TableCell>Motorcycle</TableCell>
                    <TableCell>47 mph</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>2:29 PM</TableCell>
                    <TableCell>Maple St</TableCell>
                    <TableCell>Van</TableCell>
                    <TableCell>41 mph</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}

function BellIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
      <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
    </svg>
  )
}


function LineChart(props) {
  return (
    <div {...props}>
      <ResponsiveLine
        data={[
          {
            id: "Desktop",
            data: [
              { x: "Jan", y: 43 },
              { x: "Feb", y: 137 },
              { x: "Mar", y: 61 },
              { x: "Apr", y: 145 },
              { x: "May", y: 26 },
              { x: "Jun", y: 154 },
            ],
          },
          {
            id: "Mobile",
            data: [
              { x: "Jan", y: 60 },
              { x: "Feb", y: 48 },
              { x: "Mar", y: 177 },
              { x: "Apr", y: 78 },
              { x: "May", y: 96 },
              { x: "Jun", y: 204 },
            ],
          },
        ]}
        margin={{ top: 10, right: 10, bottom: 40, left: 40 }}
        xScale={{
          type: "point",
        }}
        yScale={{
          type: "linear",
        }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 0,
          tickPadding: 16,
        }}
        axisLeft={{
          tickSize: 0,
          tickValues: 5,
          tickPadding: 16,
        }}
        colors={["#2563eb", "#e11d48"]}
        pointSize={6}
        useMesh={true}
        gridYValues={6}
        theme={{
          tooltip: {
            chip: {
              borderRadius: "9999px",
            },
            container: {
              fontSize: "12px",
              textTransform: "capitalize",
              borderRadius: "6px",
            },
          },
          grid: {
            line: {
              stroke: "#f3f4f6",
            },
          },
        }}
        role="application"
      />
    </div>
  )
}


function Package2Icon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 9h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9Z" />
      <path d="m3 9 2.45-4.9A2 2 0 0 1 7.24 3h9.52a2 2 0 0 1 1.8 1.1L21 9" />
      <path d="M12 3v6" />
    </svg>
  )
}


function SearchIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  )
}
