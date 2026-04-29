
#include "scsLexer.h"
#include "sc-memory/scs/scs_parser.hpp"

#include "sc-memory/sc_debug.hpp"

#define APPEND_ATTRS(__attrs, __edge) \
for (auto const & _a : __attrs) \
{ \
  ElementHandle const attrEdge = m_parser->ProcessConnector(_a.second ? "->" : "_->"); \
  m_parser->ProcessTriple(_a.first, attrEdge, __edge); \
}

#define PARSE_ERROR(line, pos, msg) \
  SC_THROW_EXCEPTION(utils::ExceptionParseError, \
                    "line " << line << ", " << pos << " " << msg);



// Generated from scs.g4 by ANTLR 4.7.1

#pragma once


#include "antlr4-runtime.h"


namespace scs {


class  scsParser : public antlr4::Parser {
public:
  enum {
    T__0 = 1, T__1 = 2, T__2 = 3, T__3 = 4, T__4 = 5, T__5 = 6, T__6 = 7, 
    T__7 = 8, T__8 = 9, T__9 = 10, T__10 = 11, T__11 = 12, T__12 = 13, T__13 = 14, 
    T__14 = 15, T__15 = 16, T__16 = 17, T__17 = 18, T__18 = 19, T__19 = 20, 
    T__20 = 21, T__21 = 22, T__22 = 23, T__23 = 24, T__24 = 25, T__25 = 26, 
    T__26 = 27, T__27 = 28, T__28 = 29, T__29 = 30, T__30 = 31, T__31 = 32, 
    T__32 = 33, T__33 = 34, T__34 = 35, T__35 = 36, T__36 = 37, T__37 = 38, 
    T__38 = 39, T__39 = 40, T__40 = 41, T__41 = 42, T__42 = 43, T__43 = 44, 
    T__44 = 45, T__45 = 46, T__46 = 47, T__47 = 48, T__48 = 49, T__49 = 50, 
    T__50 = 51, T__51 = 52, T__52 = 53, T__53 = 54, T__54 = 55, T__55 = 56, 
    T__56 = 57, T__57 = 58, T__58 = 59, T__59 = 60, T__60 = 61, T__61 = 62, 
    T__62 = 63, T__63 = 64, T__64 = 65, T__65 = 66, T__66 = 67, T__67 = 68, 
    T__68 = 69, T__69 = 70, T__70 = 71, ID_SYSTEM = 72, ALIAS_SYMBOLS = 73, 
    CONTOUR_BEGIN = 74, CONTOUR_END = 75, CONTENT_BODY = 76, LINK = 77, 
    EDGE_ATTR = 78, LINE_TERMINATOR = 79, LINE_COMMENT = 80, MULTINE_COMMENT = 81, 
    WS = 82
  };

  enum {
    RuleContent = 0, RuleContour = 1, RuleConnector = 2, RuleSyntax = 3, 
    RuleSentence_wrap = 4, RuleSentence = 5, RuleIdtf_alias = 6, RuleIdtf_system = 7, 
    RuleSentence_assign = 8, RuleSentence_assign_contour = 9, RuleIdtf_lvl1_preffix = 10, 
    RuleIdtf_lvl1_value = 11, RuleIdtf_lvl1 = 12, RuleIdtf_edge = 13, RuleIdtf_set = 14, 
    RuleIdtf_set_elements = 15, RuleIdtf_atomic = 16, RuleIdtf_url = 17, 
    RuleIdtf_common = 18, RuleIdtf_list = 19, RuleInternal_sentence = 20, 
    RuleInternal_sentence_list = 21, RuleSentence_lvl1 = 22, RuleSentence_lvl_4_list_item = 23, 
    RuleSentence_lvl_common = 24, RuleAttr_list = 25
  };

  scsParser(antlr4::TokenStream *input);
  ~scsParser();

  virtual std::string getGrammarFileName() const override;
  virtual const antlr4::atn::ATN& getATN() const override { return _atn; };
  virtual const std::vector<std::string>& getTokenNames() const override { return _tokenNames; }; // deprecated: use vocabulary instead.
  virtual const std::vector<std::string>& getRuleNames() const override;
  virtual antlr4::dfa::Vocabulary& getVocabulary() const override;



  public:
    void setParser(scs::Parser * parser)
    {
      m_parser = parser;
    }

  private:
    scs::Parser * m_parser;

  public:



  class ContentContext;
  class ContourContext;
  class ConnectorContext;
  class SyntaxContext;
  class Sentence_wrapContext;
  class SentenceContext;
  class Idtf_aliasContext;
  class Idtf_systemContext;
  class Sentence_assignContext;
  class Sentence_assign_contourContext;
  class Idtf_lvl1_preffixContext;
  class Idtf_lvl1_valueContext;
  class Idtf_lvl1Context;
  class Idtf_edgeContext;
  class Idtf_setContext;
  class Idtf_set_elementsContext;
  class Idtf_atomicContext;
  class Idtf_urlContext;
  class Idtf_commonContext;
  class Idtf_listContext;
  class Internal_sentenceContext;
  class Internal_sentence_listContext;
  class Sentence_lvl1Context;
  class Sentence_lvl_4_list_itemContext;
  class Sentence_lvl_commonContext;
  class Attr_listContext; 

  class  ContentContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    bool isVar = false;;
    antlr4::Token *c = nullptr;;
    ContentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CONTENT_BODY();

   
  };

  ContentContext* content();

  class  ContourContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle contourHandle = ElementHandle();
    ElementHandle handle;
    ContourContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    ContourContext(antlr4::ParserRuleContext *parent, size_t invokingState, ElementHandle contourHandle = ElementHandle());
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CONTOUR_BEGIN();
    antlr4::tree::TerminalNode *CONTOUR_END();
    std::vector<Sentence_wrapContext *> sentence_wrap();
    Sentence_wrapContext* sentence_wrap(size_t i);
    std::vector<Sentence_lvl_4_list_itemContext *> sentence_lvl_4_list_item();
    Sentence_lvl_4_list_itemContext* sentence_lvl_4_list_item(size_t i);

   
  };

  ContourContext* contour(ElementHandle contourHandle = ElementHandle());

  class  ConnectorContext : public antlr4::ParserRuleContext {
  public:
    std::string text;
    antlr4::Token *c = nullptr;;
    ConnectorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;

   
  };

  ConnectorContext* connector();

  class  SyntaxContext : public antlr4::ParserRuleContext {
  public:
    SyntaxContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EOF();
    std::vector<Sentence_wrapContext *> sentence_wrap();
    Sentence_wrapContext* sentence_wrap(size_t i);

   
  };

  SyntaxContext* syntax();

  class  Sentence_wrapContext : public antlr4::ParserRuleContext {
  public:
    Sentence_wrapContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SentenceContext *sentence();

   
  };

  Sentence_wrapContext* sentence_wrap();

  class  SentenceContext : public antlr4::ParserRuleContext {
  public:
    SentenceContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Sentence_lvl1Context *sentence_lvl1();
    Sentence_assignContext *sentence_assign();
    Sentence_assign_contourContext *sentence_assign_contour();
    Sentence_lvl_commonContext *sentence_lvl_common();

   
  };

  SentenceContext* sentence();

  class  Idtf_aliasContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    antlr4::Token *alias_symbolsToken = nullptr;;
    Idtf_aliasContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ALIAS_SYMBOLS();

   
  };

  Idtf_aliasContext* idtf_alias();

  class  Idtf_systemContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    antlr4::Token *id_systemToken = nullptr;;
    scsParser::Idtf_lvl1_preffixContext *type = nullptr;;
    Idtf_systemContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ID_SYSTEM();
    Idtf_lvl1_preffixContext *idtf_lvl1_preffix();

   
  };

  Idtf_systemContext* idtf_system();

  class  Sentence_assignContext : public antlr4::ParserRuleContext {
  public:
    antlr4::Token *alias_symbolsToken = nullptr;;
    scsParser::Idtf_commonContext *i = nullptr;;
    Sentence_assignContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ALIAS_SYMBOLS();
    Idtf_commonContext *idtf_common();

   
  };

  Sentence_assignContext* sentence_assign();

  class  Sentence_assign_contourContext : public antlr4::ParserRuleContext {
  public:
    scsParser::Idtf_systemContext *a = nullptr;;
    Sentence_assign_contourContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ContourContext *contour();
    Idtf_systemContext *idtf_system();

   
  };

  Sentence_assign_contourContext* sentence_assign_contour();

  class  Idtf_lvl1_preffixContext : public antlr4::ParserRuleContext {
  public:
    std::string text;
    antlr4::Token *type = nullptr;;
    Idtf_lvl1_preffixContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;

   
  };

  Idtf_lvl1_preffixContext* idtf_lvl1_preffix();

  class  Idtf_lvl1_valueContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    scsParser::Idtf_lvl1_preffixContext *type = nullptr;;
    antlr4::Token *i = nullptr;;
    Idtf_lvl1_valueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Idtf_lvl1_preffixContext *idtf_lvl1_preffix();
    antlr4::tree::TerminalNode *ID_SYSTEM();

   
  };

  Idtf_lvl1_valueContext* idtf_lvl1_value();

  class  Idtf_lvl1Context : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    scsParser::Idtf_lvl1_valueContext *idtf_lvl1_valueContext = nullptr;;
    Idtf_lvl1Context(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Idtf_lvl1_valueContext *idtf_lvl1_value();

   
  };

  Idtf_lvl1Context* idtf_lvl1();

  class  Idtf_edgeContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    scsParser::Idtf_atomicContext *src = nullptr;;
    scsParser::ConnectorContext *c = nullptr;;
    scsParser::Attr_listContext *attrs = nullptr;;
    scsParser::Idtf_atomicContext *trg = nullptr;;
    Idtf_edgeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Idtf_atomicContext *> idtf_atomic();
    Idtf_atomicContext* idtf_atomic(size_t i);
    ConnectorContext *connector();
    Attr_listContext *attr_list();

   
  };

  Idtf_edgeContext* idtf_edge();

  class  Idtf_setContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    scsParser::Idtf_set_elementsContext *ctx_s = nullptr;;
    scsParser::Idtf_set_elementsContext *ctx_v = nullptr;;
    Idtf_setContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Idtf_set_elementsContext *idtf_set_elements();

   
  };

  Idtf_setContext* idtf_set();

  class  Idtf_set_elementsContext : public antlr4::ParserRuleContext {
  public:
    std::string setType;
    ElementHandle handle;
    ElementHandle prevEdge;
    scsParser::Attr_listContext *a1 = nullptr;;
    scsParser::Idtf_commonContext *i1 = nullptr;;
    scsParser::Attr_listContext *a2 = nullptr;;
    scsParser::Idtf_commonContext *i2 = nullptr;;
    Idtf_set_elementsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    Idtf_set_elementsContext(antlr4::ParserRuleContext *parent, size_t invokingState, std::string setType);
    virtual size_t getRuleIndex() const override;
    std::vector<Idtf_commonContext *> idtf_common();
    Idtf_commonContext* idtf_common(size_t i);
    std::vector<Internal_sentence_listContext *> internal_sentence_list();
    Internal_sentence_listContext* internal_sentence_list(size_t i);
    std::vector<Attr_listContext *> attr_list();
    Attr_listContext* attr_list(size_t i);

   
  };

  Idtf_set_elementsContext* idtf_set_elements(std::string setType);

  class  Idtf_atomicContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    scsParser::Idtf_aliasContext *a = nullptr;;
    scsParser::Idtf_systemContext *is = nullptr;;
    Idtf_atomicContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Idtf_aliasContext *idtf_alias();
    Idtf_systemContext *idtf_system();

   
  };

  Idtf_atomicContext* idtf_atomic();

  class  Idtf_urlContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    antlr4::Token *linkToken = nullptr;;
    Idtf_urlContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LINK();

   
  };

  Idtf_urlContext* idtf_url();

  class  Idtf_commonContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle handle;
    scsParser::Idtf_atomicContext *a = nullptr;;
    scsParser::Idtf_edgeContext *ie = nullptr;;
    scsParser::Idtf_setContext *iset = nullptr;;
    scsParser::ContourContext *ct = nullptr;;
    scsParser::ContentContext *cn = nullptr;;
    scsParser::Idtf_urlContext *u = nullptr;;
    Idtf_commonContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Idtf_atomicContext *idtf_atomic();
    Idtf_edgeContext *idtf_edge();
    Idtf_setContext *idtf_set();
    ContourContext *contour();
    ContentContext *content();
    Idtf_urlContext *idtf_url();

   
  };

  Idtf_commonContext* idtf_common();

  class  Idtf_listContext : public antlr4::ParserRuleContext {
  public:
    std::vector<ElementHandle> items;
    scsParser::Idtf_commonContext *i1 = nullptr;;
    scsParser::Idtf_commonContext *i2 = nullptr;;
    Idtf_listContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Idtf_commonContext *> idtf_common();
    Idtf_commonContext* idtf_common(size_t i);
    std::vector<Internal_sentence_listContext *> internal_sentence_list();
    Internal_sentence_listContext* internal_sentence_list(size_t i);

   
  };

  Idtf_listContext* idtf_list();

  class  Internal_sentenceContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle source;
    scsParser::ConnectorContext *c = nullptr;;
    scsParser::Attr_listContext *attrs = nullptr;;
    scsParser::Idtf_listContext *targets = nullptr;;
    Internal_sentenceContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    Internal_sentenceContext(antlr4::ParserRuleContext *parent, size_t invokingState, ElementHandle source);
    virtual size_t getRuleIndex() const override;
    ConnectorContext *connector();
    Idtf_listContext *idtf_list();
    Attr_listContext *attr_list();
    Internal_sentence_listContext *internal_sentence_list();

   
  };

  Internal_sentenceContext* internal_sentence(ElementHandle source);

  class  Internal_sentence_listContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle source;
    Internal_sentence_listContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    Internal_sentence_listContext(antlr4::ParserRuleContext *parent, size_t invokingState, ElementHandle source);
    virtual size_t getRuleIndex() const override;
    std::vector<Internal_sentenceContext *> internal_sentence();
    Internal_sentenceContext* internal_sentence(size_t i);

   
  };

  Internal_sentence_listContext* internal_sentence_list(ElementHandle source);

  class  Sentence_lvl1Context : public antlr4::ParserRuleContext {
  public:
    scsParser::Idtf_lvl1Context *src = nullptr;;
    scsParser::Idtf_lvl1Context *edge = nullptr;;
    scsParser::Idtf_lvl1Context *trg = nullptr;;
    Sentence_lvl1Context(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Idtf_lvl1Context *> idtf_lvl1();
    Idtf_lvl1Context* idtf_lvl1(size_t i);

   
  };

  Sentence_lvl1Context* sentence_lvl1();

  class  Sentence_lvl_4_list_itemContext : public antlr4::ParserRuleContext {
  public:
    ElementHandle source;
    scsParser::ConnectorContext *c = nullptr;;
    scsParser::Attr_listContext *attrs = nullptr;;
    scsParser::Idtf_listContext *targets = nullptr;;
    Sentence_lvl_4_list_itemContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    Sentence_lvl_4_list_itemContext(antlr4::ParserRuleContext *parent, size_t invokingState, ElementHandle source);
    virtual size_t getRuleIndex() const override;
    ConnectorContext *connector();
    Idtf_listContext *idtf_list();
    Attr_listContext *attr_list();

   
  };

  Sentence_lvl_4_list_itemContext* sentence_lvl_4_list_item(ElementHandle source);

  class  Sentence_lvl_commonContext : public antlr4::ParserRuleContext {
  public:
    scsParser::Idtf_commonContext *src = nullptr;;
    Sentence_lvl_commonContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Sentence_lvl_4_list_itemContext *> sentence_lvl_4_list_item();
    Sentence_lvl_4_list_itemContext* sentence_lvl_4_list_item(size_t i);
    Idtf_commonContext *idtf_common();

   
  };

  Sentence_lvl_commonContext* sentence_lvl_common();

  class  Attr_listContext : public antlr4::ParserRuleContext {
  public:
    std::vector<std::pair<ElementHandle, bool>> items;
    antlr4::Token *id_systemToken = nullptr;;
    antlr4::Token *edge_attrToken = nullptr;;
    Attr_listContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> ID_SYSTEM();
    antlr4::tree::TerminalNode* ID_SYSTEM(size_t i);
    std::vector<antlr4::tree::TerminalNode *> EDGE_ATTR();
    antlr4::tree::TerminalNode* EDGE_ATTR(size_t i);

   
  };

  Attr_listContext* attr_list();


private:
  static std::vector<antlr4::dfa::DFA> _decisionToDFA;
  static antlr4::atn::PredictionContextCache _sharedContextCache;
  static std::vector<std::string> _ruleNames;
  static std::vector<std::string> _tokenNames;

  static std::vector<std::string> _literalNames;
  static std::vector<std::string> _symbolicNames;
  static antlr4::dfa::Vocabulary _vocabulary;
  static antlr4::atn::ATN _atn;
  static std::vector<uint16_t> _serializedATN;


  struct Initializer {
    Initializer();
  };
  static Initializer _init;
};

}  // namespace scs
