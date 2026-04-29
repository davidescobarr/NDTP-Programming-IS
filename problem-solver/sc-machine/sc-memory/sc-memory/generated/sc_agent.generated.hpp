#include <memory>

#include "sc-memory/sc_memory.hpp"


#include "sc-memory/sc_event.hpp"




#define sc_agent_hpp_25_init  bool _InitInternal(ScAddr const & outputStructure = ScAddr::Empty) override \
{ \
    ScMemoryContext ctx(sc_access_lvl_make_min, "ScAgent::_InitInternal"); \
    ScSystemIdentifierFiver fiver; \
    bool result = true; \
     \
    return result; \
}


#define sc_agent_hpp_25_initStatic static bool _InitStaticInternal(ScAddr const & outputStructure = ScAddr::Empty)  \
{ \
    ScMemoryContext ctx(sc_access_lvl_make_min, "ScAgent::_InitStaticInternal"); \
    ScSystemIdentifierFiver fiver; \
    bool result = true; \
    return result; \
}


#define sc_agent_hpp_25_decl 

#define sc_agent_hpp_ScAgent_impl 

#define sc_agent_hpp_43_init  bool _InitInternal(ScAddr const & outputStructure = ScAddr::Empty) override \
{ \
    ScMemoryContext ctx(sc_access_lvl_make_min, "ScAgentAction::_InitInternal"); \
    ScSystemIdentifierFiver fiver; \
    bool result = true; \
     \
    return result; \
}


#define sc_agent_hpp_43_initStatic static bool _InitStaticInternal(ScAddr const & outputStructure = ScAddr::Empty)  \
{ \
    ScMemoryContext ctx(sc_access_lvl_make_min, "ScAgentAction::_InitStaticInternal"); \
    ScSystemIdentifierFiver fiver; \
    bool result = true; \
    return result; \
}


#define sc_agent_hpp_43_decl 

#define sc_agent_hpp_ScAgentAction_impl 

#undef ScFileID
#define ScFileID sc_agent_hpp

