"""Local tests; no credentials or external calls."""
import base64, io, json, threading, unittest, urllib.request, urllib.error
from unittest.mock import patch
import server

class TestGemini(unittest.TestCase):
    def setUp(self):
        server.CALLS.clear(); server.DAY_CALLS.clear()
        self.s=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        self.t=threading.Thread(target=self.s.serve_forever,daemon=True); self.t.start()
        self.url='http://127.0.0.1:'+str(self.s.server_port)
    def tearDown(self):
        self.s.shutdown(); self.s.server_close(); self.t.join()
    def request(self,path,body=None,auth=True):
        headers={'Content-Type':'application/json'}
        if auth: headers['Authorization']='Basic '+base64.b64encode(b'ismael:TestPassword12345678').decode()
        req=urllib.request.Request(self.url+path,data=None if body is None else json.dumps(body).encode(),headers=headers)
        try:
            with urllib.request.build_opener().open(req) as r: return r.status,json.load(r)
        except urllib.error.HTTPError as e:
            return e.code,json.load(e) if e.code!=401 else {}
    @patch.object(server,'PASSWORD','TestPassword12345678')
    @patch.object(server,'USERNAME','ismael')
    @patch.object(server,'KEY','fake-key-not-real')
    def test_text_and_image(self):
        self.assertEqual(self.request('/api/status',auth=False)[0],401)
        self.assertEqual(self.request('/healthz',auth=False)[0],200)
        status,d=self.request('/api/status'); self.assertEqual(d['version'],'2.0'); self.assertNotIn('fake-key',str(d))
        def fake(req,timeout):
            self.assertIn(':generateContent',req.full_url); self.assertEqual(req.get_header('X-goog-api-key'),'fake-key-not-real')
            body=json.loads(req.data); self.assertIn('systemInstruction',body)
            self.assertEqual(body['contents'][0]['parts'][1]['inlineData']['mimeType'],'image/jpeg')
            return io.BytesIO(json.dumps({'candidates':[{'content':{'parts':[{'text':'["Super robot !"]'}]}}]}).encode())
        with patch.object(server.urllib.request,'urlopen',side_effect=fake):
            status,d=self.request('/api/comments',{'latest':'Mon robot','image':'data:image/jpeg;base64,'+base64.b64encode(b'\xff\xd8test').decode()})
            self.assertEqual((status,d),(200,{'comments':['Super robot !']}))
            self.assertEqual(self.request('/api/comments',{})[0],429)
    @patch.object(server,'PASSWORD','')
    @patch.object(server,'KEY','fake-key-not-real')
    def test_quota(self):
        error=urllib.error.HTTPError('https://example.invalid',429,'quota',{},None)
        with patch.object(server.urllib.request,'urlopen',side_effect=error):
            status,d=self.request('/api/comments',{'latest':'bonjour'}); self.assertEqual(status,429); self.assertEqual(d['retry_after'],60)
    @patch.object(server,'PASSWORD','')
    @patch.object(server,'KEY','')
    def test_no_key(self):
        self.assertEqual(self.request('/api/comments',{})[0],503)
if __name__=='__main__': unittest.main()
