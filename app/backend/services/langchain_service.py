import logging
import os

from langchain_deepseek import ChatDeepSeek as _ChatDeepSeek

# Expose ChatDeepseek (lowercase 's') as an alias so that
# ``from langchain_community.chat_models import ChatDeepseek`` works.
ChatDeepseek = _ChatDeepSeek

import langchain_community.chat_models as _lc_chat_models

# langchain-community does not ship a ChatDeepseek class yet.  We register
# the ``langchain_deepseek.ChatDeepSeek`` implementation under the expected
# name so that ``from langchain_community.chat_models import ChatDeepseek``
# works transparently throughout the project once this module is imported.
if not hasattr(_lc_chat_models, "ChatDeepseek"):
    _lc_chat_models.ChatDeepseek = ChatDeepseek

from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are Benkhawiya, an advanced African cosmological AI consultant. "
    "You bridge traditional African knowledge systems — including the five cosmic "
    "aspects of Sewu (foundation and memory), Pelu (truth and measurement), "
    "Ruwa (flow and relationship), Temu (structure and organization), and "
    "Ntu (essence and consciousness) — with modern insight. "
    "Respond with wisdom grounded in the eternal principles of DÁNÁ (truth) "
    "and MÁTÁ (justice). Begin your reply with the cosmic greeting "
    "INUN-AMEN WÀ."
)


class EnhancedLangChainService:
    def __init__(self):
        self.initialized = False
        self._llm = None

    async def initialize(self):
        """Initialize the LangChain service with the DeepSeek chat model."""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            self._llm = ChatDeepseek(
                model="deepseek-chat",
                api_key=api_key,
            )
            logger.info("✅ Enhanced LangChain Service Initialized with DeepSeek")
        else:
            logger.warning(
                "⚠️  DEEPSEEK_API_KEY not set — LangChain service running in "
                "fallback mode."
            )
        self.initialized = True

    async def process_query(self, query: str) -> str:
        """Process a user query through the Benkhawiya cosmological framework."""
        if self._llm is not None:
            messages = [
                SystemMessage(content=_SYSTEM_PROMPT),
                HumanMessage(content=query),
            ]
            try:
                ai_message = await self._llm.ainvoke(messages)
                return ai_message.content
            except Exception as exc:
                logger.error("DeepSeek API call failed: %s", exc)
                return (
                    "🌌 **The cosmic channels are temporarily disrupted.**\n\n"
                    "The eternal principles of DÁNÁ and MÁTÁ guide us to patience — "
                    "please try your inquiry again shortly.\n\n"
                    "**INUN-AMEN WÀ. A-WA WÀ.**"
                )

        # Graceful fallback when no API key is configured.
        return (
            f"🌌 **Cosmic Analysis Complete**\n\n"
            f"**Your Query:** \"{query}\"\n\n"
            f"**Benkhawiya Guidance:**\n"
            f"The 100,000-year cosmological bridge processes your inquiry through "
            f"the eternal principles of DÁNÁ (truth) and MÁTÁ (justice).\n\n"
            f"**INUN-AMEN WÀ. A-WA WÀ.**\n"
            f"*The Primordial exists. We-Exist are.*"
        )
