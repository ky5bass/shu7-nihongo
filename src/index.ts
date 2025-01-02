// https://www.to-r.net/media/cloudflare-pages-basic/ をコピペ
// ↑をエラー出ないよう修正
// ↑を関数をインライン展開
// ↑を認証の成否に関する処理を合理化
// ↑をWorkers Site化

/**
 * Shows how to restrict access using the HTTP Basic schema.
 * @see https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication
 * @see https://tools.ietf.org/html/rfc7617
 *
 * A user-id containing a colon (":") character is invalid, as the
 * first colon in a user-pass string separates user and password.
 */

import { getAssetFromKV } from "@cloudflare/kv-asset-handler";
import manifestJSON from "__STATIC_CONTENT_MANIFEST";
const assetManifest = JSON.parse(manifestJSON);
/* 参考 https://developers.cloudflare.com/workers/configuration/sites/start-from-worker/ */

const encoder = new TextEncoder();

/**
 * Protect against timing attacks by safely comparing values using `timingSafeEqual`.
 * Refer to https://developers.cloudflare.com/workers/runtime-apis/web-crypto/#timingsafeequal for more details
*/
function timingSafeEqual(a: string, b: string) {
  const aBytes = encoder.encode(a);
  const bBytes = encoder.encode(b);
  
  if (aBytes.byteLength !== bBytes.byteLength) {
    // Strings must be the same length in order to compare
    // with crypto.subtle.timingSafeEqual
    return false;
  }
  
  return crypto.subtle.timingSafeEqual(aBytes, bBytes);
}

/**
 * Receives a HTTP request and replies with a response.
 * @param {Request} request
 * @returns {Promise<Response>}
*/
interface Env {
  SH7N_USER:     string;
  SH7N_PASSWORD: string;
  __STATIC_CONTENT: KVNamespace<string>;
}
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const BASIC_USER = env.SH7N_USER;
    
    // You will need an admin password. This should be
    // attached to your Worker as an encrypted secret.
    // Refer to https://developers.cloudflare.com/workers/configuration/secrets/
    const BASIC_PASS = env.SH7N_PASSWORD;
    
    // The "Authorization" header is sent when authenticated.
    if (request.headers.has("Authorization")) {
      const { user, pass } = basicAuthentication(request);
      
      if (
        timingSafeEqual(BASIC_USER, user) &&
        timingSafeEqual(BASIC_PASS, pass)
      ) {
        // 認証に成功した場合、アセットのコンテンツをリターン
        try {
          return await getAssetFromKV(
            {
              request,
              waitUntil: ctx.waitUntil.bind(ctx),
            },
            {
              ASSET_NAMESPACE: env.__STATIC_CONTENT,
              ASSET_MANIFEST: assetManifest,
            },
          );
        } catch (e) {
          let pathname = new URL(request.url).pathname;
          return new Response(`"${pathname}" not found`, {
            status: 404,
            statusText: "not found",
          });
        }
        /* 参考 https://developers.cloudflare.com/workers/configuration/sites/start-from-worker/ */
      }
    }

    // 認証に失敗または未認証の場合、401をリターン
    return new Response("Invalid credentials.", {
      status: 401,
      headers: {
        // Prompts the user for credentials.
        "WWW-Authenticate": 'Basic realm="my scope", charset="UTF-8"',
      },
    });
  },
} satisfies ExportedHandler<Env>;

/**
 * Parse HTTP Basic Authorization value.
 * @param {Request} request
 * @throws {BadRequestException}
 * @returns {{ user: string, pass: string }}
 */
function basicAuthentication(request: Request) {
  const authorization = request.headers.get("Authorization")!;

  const [scheme, encoded] = authorization.split(" ");

  // The Authorization header must start with Basic, followed by a space.
  if (!encoded || scheme !== "Basic") {
    throw new BadRequestException("Malformed authorization header.");
  }

  // Decodes the base64 value and performs unicode normalization.
  // @see https://datatracker.ietf.org/doc/html/rfc7613#section-3.3.2 (and #section-4.2.2)
  // @see https://dev.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/normalize
  const buffer = Uint8Array.from(atob(encoded), character => character.charCodeAt(0));
  const decoded = new TextDecoder().decode(buffer).normalize();

  // The username & password are split by the first colon.
  //=> example: "username:password"
  const index = decoded.indexOf(":");

  // The user & password are split by the first colon and MUST NOT contain control characters.
  // @see https://tools.ietf.org/html/rfc5234#appendix-B.1 (=> "CTL = %x00-1F / %x7F")
  if (index === -1 || /[\0-\x1F\x7F]/.test(decoded)) {
    throw new BadRequestException("Invalid authorization value.");
  }

  return {
    user: decoded.substring(0, index),
    pass: decoded.substring(index + 1),
  };
}

class BadRequestException {
  status: number;
  statusText: string;
  reason: string;

  constructor(reason: string) {
    this.status = 400;
    this.statusText = "Bad Request";
    this.reason = reason;
  }
}

addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request).catch(err => {
      const message = err.reason || err.stack || "Unknown Error";

      return new Response(message, {
        status: err.status || 500,
        statusText: err.statusText || null,
        headers: {
          "Content-Type": "text/plain;charset=UTF-8",
          // Disables caching by default.
          "Cache-Control": "no-store",
          // Returns the "Content-Length" header for HTTP HEAD requests.
          "Content-Length": message.length,
        },
      });
    })
  );
});