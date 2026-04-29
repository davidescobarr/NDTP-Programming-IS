#include <memory>

#include "sc-memory/sc_memory.hpp"


#include "sc-memory/sc_event.hpp"




#define DirectInferenceAgent_hpp_21_init  bool _InitInternal(ScAddr const & outputStructure = ScAddr::Empty) override \
{ \
    ScMemoryContext ctx(sc_access_lvl_make_min, "DirectInferenceAgent::_InitInternal"); \
    ScSystemIdentifierFiver fiver; \
    bool result = true; \
    return result; \
}


#define DirectInferenceAgent_hpp_21_initStatic static bool _InitStaticInternal(ScAddr const & outputStructure = ScAddr::Empty)  \
{ \
    ScMemoryContext ctx(sc_access_lvl_make_min, "DirectInferenceAgent::_InitStaticInternal"); \
    ScSystemIdentifierFiver fiver; \
    bool result = true; \
    return result; \
}


#define DirectInferenceAgent_hpp_21_decl \
private:\
	typedef ScAgent Super;\
protected: \
	DirectInferenceAgent(char const * name, sc_uint8 accessLvl) : Super(name, accessLvl) {}\
	virtual sc_result Run(ScAddr const & listenAddr, ScAddr const & edgeAddr, ScAddr const & otherAddr) override; \
private:\
	static std::unique_ptr<ScEvent> ms_event;\
    static std::unique_ptr<ScMemoryContext> ms_context;\
public: \
	static bool handler_emit(ScAddr const & addr, ScAddr const & edgeAddr, ScAddr const & otherAddr)\
	{\
		DirectInferenceAgent Instance("DirectInferenceAgent", sc_access_lvl_make_min);\
		return Instance.Run(addr, edgeAddr, otherAddr) == SC_RESULT_OK;\
	}\
	static void RegisterHandler()\
	{\
		ms_context.reset(new ScMemoryContext(sc_access_lvl_make_min, "handler_DirectInferenceAgent"));\
		ms_event.reset(new ScEvent(*ms_context, InferenceKeynodes::action_direct_inference, ScEvent::Type::AddOutputEdge, &DirectInferenceAgent::handler_emit));\
        if (ms_event.get())\
        {\
            SC_LOG_INFO("Register agent DirectInferenceAgent");\
        }\
        else\
        {\
            SC_LOG_ERROR("Can't register agent DirectInferenceAgent");\
        }\
	}\
	static void UnregisterHandler()\
	{\
		ms_event.reset();\
		ms_context.reset();\
	}

#define DirectInferenceAgent_hpp_DirectInferenceAgent_impl \
std::unique_ptr<ScEvent> DirectInferenceAgent::ms_event;\
std::unique_ptr<ScMemoryContext> DirectInferenceAgent::ms_context;

#undef ScFileID
#define ScFileID DirectInferenceAgent_hpp

