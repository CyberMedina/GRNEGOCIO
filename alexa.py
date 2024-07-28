# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

import requests
from requests.exceptions import Timeout
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.dialog import ElicitSlotDirective
from ask_sdk_model.intent import Intent

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ""
        reprompt_text = "¿Necesitas algo más?"

        try:
            response = requests.get('https://grmedina.pythonanywhere.com/pruebita', timeout=60)
            if response.status_code == 200:
                speak_output = "¡Hola!, Bienvenido al negocio, ¿en qué puedo ayudarte hoy?"
            else:
                speak_output = "Hmmm hubo un error al conectarme a la base de datos de los clientes, intenta más tarde"
        except Timeout:
            speak_output = "Hmmm hubo un error al conectarme al sistema"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)  # Agrega esto para mantener la sesión abierta
                .response
        )

class GetCapitalIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("busqueda_capital_intent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        person = handler_input.request_envelope.request.intent.slots["nombres"].value

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = 'https://grmedina.pythonanywhere.com/api/obtener_estadoCliente'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class cantidadPagoClienteIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("cantidadPagoClienteIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        person = handler_input.request_envelope.request.intent.slots["cliente"].value

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = 'https://grmedina.pythonanywhere.com/api/obtener_cantidad_pago_cliente'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class obtener_cantidad_clientes_pagadosIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("obtener_cantidad_clientes_pagadosIntent")(handler_input)

    def handle(self, handler_input):

        # Aquí es donde haces la solicitud GET a tu API
        url = 'https://grmedina.pythonanywhere.com/api/obtener_cantidad_clientes_pagados'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )
        
class obtener_cantidad_total_dinero_quincenal_clientesIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("obtener_cantidad_total_dinero_quincenal_clientesIntent")(handler_input)

    def handle(self, handler_input):

        # Aquí es donde haces la solicitud GET a tu API
        url = 'https://grmedina.pythonanywhere.com/api/obtener_cantidad_total_dinero_quincenal_clientes'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class enviar_correo_intent(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("enviar_correo_intent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        person = handler_input.request_envelope.request.intent.slots["cliente"].value

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = 'https://grmedina.pythonanywhere.com/api/imprimir_pago_alexa'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )
        
        
class obtener_cantidad_clientes_pagadosIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("obtener_cantidad_clientes_pagadosIntent")(handler_input)

    def handle(self, handler_input):

        # Aquí es donde haces la solicitud GET a tu API
        url = 'https://grmedina.pythonanywhere.com/api/obtener_cantidad_clientes_pagados'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )
        
        
class agendarPagoNormalIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("agendarPagoNormalIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        person = handler_input.request_envelope.request.intent.slots["cliente"].value

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = 'https://qq37ws9m-5000.use.devtunnels.ms/api/agendarPagoNormal'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            
            data_json = response.json()  # Asume que la respuesta es JSON
            
            if data_json['respuesta']['estado'] == 2:
                message = f"Según mis registros el cliente {data_json['respuesta']['nombres_apellidos_cliente']} debe de pagar {data_json['respuesta']['cifra']} dólares, ¿Está seguro que desea guardar ese pago?"
                speak_output = message
                
            else:
                speak_output = "El cliente ya tiene registrado un pago en esta quincena!"
                
            
            
            
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )
        

class ConsultaPagoIntentHandler(AbstractRequestHandler):
    """Handler for Consulta Pago Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        can_handle = ask_utils.is_intent_name("consultaPagoIntent")(handler_input)
        logger.debug(f"ConsultaPagoIntentHandler can_handle: {can_handle}")
        return can_handle

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("Handling ConsultaPagoIntent")

        slots = handler_input.request_envelope.request.intent.slots
        person = slots["cliente"].value
        logger.debug(f"Slot 'cliente' value: {person}")

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = 'https://grmedina.pythonanywhere.com/api/obtener_pago'
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            logger.debug(f"API response: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error durante la solicitud a la API: {e}")
            speak_output = "Lo siento, hubo un problema al obtener los datos. Por favor intenta más tarde."
            return handler_input.response_builder.speak(speak_output).ask("¿Necesitas algo más?").response

        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            logger.debug(f"JSON response: {data_json}")
            speak_output = data_json['respuesta']
            
            # Pregunta si desea registrar el pago completo
            reprompt_text = "¿Desea registrar el pago completo? Responde sí o no."
            speak_output += " " + reprompt_text
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(
                        slot_to_elicit="registrar_pago_completo"
                    ))
                    .response
            )
        else:
            logger.warning(f"Person '{person}' not found in database")
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos. ¿Necesitas algo más?"
            return handler_input.response_builder.speak(speak_output).ask("¿Necesitas algo más?").response


class RegistrarPagoCompletoIntentHandler(AbstractRequestHandler):
    """Handler for Registrar Pago Completo Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        can_handle = ask_utils.is_intent_name("RegistrarPagoCompletoIntent")(handler_input)
        logger.debug(f"RegistrarPagoCompletoIntentHandler can_handle: {can_handle}")
        return can_handle

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.debug("Handling RegistrarPagoCompletoIntent")

        slots = handler_input.request_envelope.request.intent.slots
        registrar_pago_completo = slots["registrar_pago_completo"].value.lower()
        logger.debug(f"Slot 'registrar_pago_completo' value: {registrar_pago_completo}")

        if "sí" in registrar_pago_completo or "si" in registrar_pago_completo:
            logger.debug("User chose to register full payment")
            # Hacer POST al endpoint para registrar pago completo
            try:
                response = requests.post("https://qq37ws9m-5000.use.devtunnels.ms/api/registrar_pago_completo", json={})
                response.raise_for_status()
                logger.debug("Pago completo registrado exitosamente")
                speak_output = "Pago completo registrado exitosamente. ¿Necesitas algo más?"
                return handler_input.response_builder.speak(speak_output).ask("¿Necesitas algo más?").response
            except requests.exceptions.RequestException as e:
                logger.error(f"Error durante la solicitud a la API: {e}")
                speak_output = "Lo siento, hubo un problema al registrar el pago completo. Por favor intenta más tarde."
                return handler_input.response_builder.speak(speak_output).ask("¿Necesitas algo más?").response

        elif "no" in registrar_pago_completo:
            logger.debug("User chose not to register full payment")
            # Preguntar por el monto
            speak_output = "¿Cuál es el monto que deseas registrar?"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("Por favor, dime el monto que deseas registrar.")
                    .add_directive(ElicitSlotDirective(
                        slot_to_elicit="monto_a_registrar"
                    ))
                    .response
            )
        else:
            logger.warning("No entendí la respuesta del usuario")
            speak_output = "No entendí tu respuesta. ¿Deseas registrar el pago completo? Por favor, responde sí o no."
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class RegistrarMontoIntentHandler(AbstractRequestHandler):
    """Handler for Registrar Monto Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RegistrarMontoIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        monto = slots["monto_a_registrar"].value

        # Hacer POST al endpoint para registrar monto parcial
        try:
            response = requests.post("https://your-endpoint.com/registrar_monto", json={"monto": monto})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error durante la solicitud a la API: {e}")
            speak_output = "Lo siento, hubo un problema al registrar el monto. Por favor intenta más tarde."
            return handler_input.response_builder.speak(speak_output).response

        speak_output = f"Monto de {monto} registrado exitosamente. ¿Necesitas algo más?"
        return handler_input.response_builder.speak(speak_output).ask("¿Necesitas algo más?").response





class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Está bien, que pases un lindo día!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
        
        


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetCapitalIntentHandler())
sb.add_request_handler(enviar_correo_intent())
sb.add_request_handler(ConsultaPagoIntentHandler())
sb.add_request_handler(RegistrarPagoCompletoIntentHandler())
sb.add_request_handler(RegistrarMontoIntentHandler())
sb.add_request_handler(cantidadPagoClienteIntentHandler())
sb.add_request_handler(obtener_cantidad_clientes_pagadosIntentHandler())
sb.add_request_handler(obtener_cantidad_total_dinero_quincenal_clientesIntentHandler())
sb.add_request_handler(agendarPagoNormalIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()