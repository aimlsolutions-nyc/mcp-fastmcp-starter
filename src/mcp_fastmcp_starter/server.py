from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="mcp-fastmcp-starter", version="0.1.0")

class SayHelloIn(BaseModel):
    name: str = Field(..., min_length=1, description="Name to greet.")

class SayHelloOut(BaseModel):
    message: str
    ts_unix: float

class ReverseIn(BaseModel):
    text: str = Field(..., min_length=1, description="Text to reverse.")

class ReverseOut(BaseModel):
    reversed: str
    length: int

@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: Dict[str, Any]

def _schema(model: type[BaseModel]) -> Dict[str, Any]:
    return model.model_json_schema()

TOOLS: Dict[str, ToolSpec] = {
    "sayHello": ToolSpec(
        name="sayHello",
        description="Return a greeting message with a timestamp.",
        input_schema=_schema(SayHelloIn),
    ),
    "reverse": ToolSpec(
        name="reverse",
        description="Reverse the provided text and return the length.",
        input_schema=_schema(ReverseIn),
    ),
}

@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok"}

@app.get("/tools")
def list_tools() -> Dict[str, Any]:
    return {
        "tools": [asdict(spec) for spec in TOOLS.values()],
        "protocol_hint": "mcp-like: list tools and invoke by name with typed JSON input",
    }

class InvokeReq(BaseModel):
    tool: str
    args: Dict[str, Any] = Field(default_factory=dict)
    trace_id: Optional[str] = None

class InvokeResp(BaseModel):
    tool: str
    ok: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    trace_id: Optional[str] = None

@app.post("/invoke", response_model=InvokeResp)
def invoke(req: InvokeReq) -> InvokeResp:
    try:
        if req.tool == "sayHello":
            parsed = SayHelloIn.model_validate(req.args)
            out = SayHelloOut(message=f"Hello, {parsed.name}.", ts_unix=time.time())
            return InvokeResp(tool=req.tool, ok=True, result=out.model_dump(), trace_id=req.trace_id)

        if req.tool == "reverse":
            parsed = ReverseIn.model_validate(req.args)
            out = ReverseOut(reversed=parsed.text[::-1], length=len(parsed.text))
            return InvokeResp(tool=req.tool, ok=True, result=out.model_dump(), trace_id=req.trace_id)

        return InvokeResp(tool=req.tool, ok=False, error=f"Unknown tool: {req.tool}", trace_id=req.trace_id)

    except Exception as e:
        return InvokeResp(tool=req.tool, ok=False, error=str(e), trace_id=req.trace_id)
