import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<800"]
  }
};

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:5000";

export default function () {
  const res = http.get(`${BASE_URL}/books`);
  check(res, {
    "GET /books status is 200": (r) => r.status === 200,
    "response has books": (r) => r.body && r.body.includes("books")
  });
  sleep(1);
}
