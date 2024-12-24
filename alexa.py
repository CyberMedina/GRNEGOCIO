# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

import requests
import pytz
from datetime import datetime
from requests.exceptions import Timeout
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.dialog import ElicitSlotDirective
from ask_sdk_model.intent import Intent
from ask_sdk_core.utils import is_intent_name, get_supported_interfaces
from ask_sdk_core.utils import is_request_type
from ask_sdk_core.utils import get_supported_interfaces
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from ask_sdk_model.ui import SimpleCard

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

URL_API = "https://grmedina.pythonanywhere.com"

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # Definir la zona horaria de Managua
        managua_tz = pytz.timezone('America/Managua')
        current_time = datetime.now(managua_tz)
        hour = current_time.hour

        if 5 <= hour < 12:
            greeting = "¡Buenos días!"
        elif 12 <= hour < 18:
            greeting = "¡Buenas tardes!"
        else:
            greeting = "¡Buenas noches!"

        speak_output = ""
        reprompt_text = "¿Necesitas algo más?"

        try:
            response = requests.get(f'{URL_API}/pruebita', timeout=300)
            if response.status_code == 200:
                speak_output = f"{greeting} Bienvenido al negocio, ¿en qué puedo ayudarte hoy?"
            else:
                speak_output = "Hmmm, hubo un error al conectarme a la base de datos de los clientes, intenta más tarde."
        except Timeout:
            speak_output = "Hmmm, hubo un error al conectarme al sistema."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)  # Mantener la sesión abierta
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
        url = f'{URL_API}/api/obtener_estadoCliente'
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
        url = f'{URL_API}/api/obtener_cantidad_pago_cliente'
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
        url = f'{URL_API}/api/obtener_cantidad_clientes_pagados'
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
                .set_should_end_session(True)  # Indica que la sesión debe terminar
                .response  # Construye y devuelve la respuesta final
        )
        
class obtener_cantidad_total_dinero_quincenal_clientesIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("obtener_cantidad_total_dinero_quincenal_clientesIntent")(handler_input)

    def handle(self, handler_input):

        # Aquí es donde haces la solicitud GET a tu API
        url = f'{URL_API}/api/obtener_cantidad_total_dinero_quincenal_clientes'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ��Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)  # Indica que la sesión debe terminar
                .response  # Construye y devuelve la respuesta final
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
        url = f'{URL_API}/api/imprimir_pago_alexa'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data, timeout=10)  # Timeout de 10 segundos
        
        reprompt_text = "¿Necesitas algo más?"
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            speak_output = data_json['respuesta']
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos.  <break time='1s'/> ¿Necesitas algo más?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)  # Indica que la sesión debe terminar
                .response  # Construye y devuelve la respuesta final
        )
        
        
class obtener_cantidad_clientes_pagadosIntentHandler(AbstractRequestHandler):
    """Handler for Get Capital Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("obtener_cantidad_clientes_pagadosIntent")(handler_input)

    def handle(self, handler_input):

        # Aquí es donde haces la solicitud GET a tu API
        url = f'{URL_API}/api/obtener_cantidad_clientes_pagados'
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
    """Handler for agendarPagoNormal Intent."""
    def can_handle(self, handler_input):
        return is_intent_name("agendarPagoNormalIntent")(handler_input)

    def handle(self, handler_input):
        person = handler_input.request_envelope.request.intent.slots["cliente"].value

        # Aquí es donde haces la solicitud POST a tu API
        data = {'person': person}
        url = f'{URL_API}/api/agendarPagoNormal'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            data_json = response.json()  # Asume que la respuesta es JSON
            
            if data_json['respuesta']['estado'] == 2:
                message = f"Según mis registros el cliente {data_json['respuesta']['nombres_apellidos_cliente']} debe de pagar en la quincena {data_json['respuesta']['cifra_cordobas']} córdobas con una tasa de cambio de{data_json['respuesta']['tasa_cambio']}. El equivlante en dolares es {data_json['respuesta']['cifra']} dólares.  ¿Está seguro que desea guardar ese pago?"
                # Agregar tarjeta SimpleCard
                handler_input.response_builder.set_card(
                    SimpleCard(
                        title= f"{data_json['respuesta']['nombres_apellidos_cliente']}",
                        content= f"C$ {data_json['respuesta']['cifra_cordobas']} córdobas o $ {data_json['respuesta']['cifra']} dólares",
                    )
                )
                handler_input.attributes_manager.session_attributes["last_message"] = message
                handler_input.attributes_manager.session_attributes["last_intent"] = "agendarPagoNormalIntent"
                handler_input.attributes_manager.session_attributes["id_cliente"] = data_json['respuesta']['id_cliente']
                handler_input.attributes_manager.session_attributes["cifra"] = data_json['respuesta']['cifra']
                
                
                return (
                    handler_input.response_builder
                        .speak(message)
                        .ask("Por favor, responde sí o no.")
                        .response
                )
            else:
                session_attributes = handler_input.attributes_manager.session_attributes
                # Eliminar last_intent de la sesión después de manejarlo
                session_attributes.pop("id_cliente", None)
                session_attributes.pop("cifra", None)
                session_attributes.pop("last_intent", None)
                speak_output = "El cliente ya tiene registrado un pago en esta quincena!"
        else:
            speak_output = f"Lo siento, no encuentro a {person} en la base de datos."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)  # Indica que la sesión debe terminar
                .response  # Construye y devuelve la respuesta final
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
                speak_output = "muy bien!. acabo de guardar el pago. ¿Necesitas algo más?"
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


class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        last_intent = session_attributes.get("last_intent")
        speak_output = "No hay ninguna acción pendiente de confirmación."

        if last_intent == "agendarPagoNormalIntent":
            id_cliente = session_attributes.get("id_cliente")
            cifra = session_attributes.get("cifra")
            
            # Enviar POST request al endpoint
            url = f'{URL_API}/api/procesarPagoNormal'
            headers = {'Content-Type': 'application/json'}
            data = {
                'id_cliente': id_cliente,
                'cifra': cifra
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                speak_output = "El pago ha sido guardado exitosamente."
            except requests.exceptions.RequestException as e:
                speak_output = f"Hubo un problema al guardar el pago: {str(e)}. ¿Necesitas algo más?"
                
        elif last_intent == "OtroIntent":
            # Lógica para OtroIntent
            speak_output = "Has confirmado la acción para OtroIntent."

        # Eliminar last_intent de la sesión después de manejarlo
        session_attributes.pop("id_cliente", None)
        session_attributes.pop("cifra", None)
        session_attributes.pop("last_intent", None)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class NoIntentHandler(AbstractRequestHandler):
    """Handler for No Intent."""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        last_intent = session_attributes.get("last_intent")
        speak_output = "No hay ninguna acción pendiente de confirmación."

        if last_intent == "agendarPagoNormalIntent":
            speak_output = "Está bien!, qué otra gestión necesitas realizar?"
            return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)  # Indica que la sesión debe terminar
                .response  # Construye y devuelve la respuesta final
        )
        elif last_intent == "OtroIntent":
            speak_output = "Acción cancelada para OtroIntent. ¿Necesitas algo más?"

        # Eliminar last_intent de la sesión después de manejarlo
        session_attributes.pop("id_cliente", None)
        session_attributes.pop("cifra", None)
        session_attributes.pop("last_intent", None)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("¿Necesitas algo más?")
                .response
        )




class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Puedes decirme por ejemplo: Agenda un pago a alexa, cuanto es el saldo de alexa , cual es el estado de alexa, cuanta gente ha pagado, o cual es el total que se ha generado en la quincena. ¿Qué necesitas que haga?"

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
        # Definir la zona horaria de Managua
        managua_tz = pytz.timezone('America/Managua')
        current_time = datetime.now(managua_tz)
        hour = current_time.hour

        if 5 <= hour < 12:
            greeting = "un buen día"
        elif 12 <= hour < 18:
            greeting = "una buena tarde"
        else:
            greeting = "una buena noche"
        speak_output = f"Está bien, ¡que pases {greeting}!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)  # Indica que la sesión debe terminar
                .response  # Construye y devuelve la respuesta final
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, no entendí que quieres que haga, puedes decirme por ejemplo: Agenda un pago a alexa, cuanto es el saldo de alexa , cual es el estado de alexa, o cual es el total que se ha generado en la quincena"
        reprompt = "No entendí eso, en qué puedo ayudarte?"

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

        speak_output = "Lo siento, no entendí lo que acabas de decir, repitelo de nuevo por favor"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DineroGeneradoQuincenaActualHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DineroGeneradoQuincenaActualIntent")(handler_input)

    def handle(self, handler_input):
        url = f'{URL_API}/api/obtener_cantidad_total_dinero_quincenal_clientes'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            data = response.json()
            respuesta = data.get('respuesta', 'No se pudo obtener la información.')
            # Usar SSML para hacer que Alexa hable más lentamente y suene más natural
            speak_output = f"<speak><prosody rate='slow'>{respuesta}</prosody></speak>"
            
            # Agregar tarjeta SimpleCard
            handler_input.response_builder.set_card(
                SimpleCard(
                    title="Dinero Generado",
                    content=respuesta
                )
            )
            # Agregar un reprompt para mantener la sesión abierta
            reprompt_text = "¿Quieres saber algo más?"
        else:
            speak_output = "<speak>Lo siento, no pude obtener la información.</speak>"
            reprompt_text = "¿Necesitas ayuda con otra consulta?"
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)  # Indica que la sesión debe terminar
                .response  # Construye y devuelve la respuesta final
        )
        
        
class ObtenerClientesPagadosHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ObtenerClientesPagadosIntent")(handler_input)

    def handle(self, handler_input):
        url = f'{URL_API}/api/obtener_clientes_pagados'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            data = response.json()
            respuesta = data.get('respuesta', {})
            alexa_speak = respuesta.get('alexa_speak', 'No se pudo obtener la información.')
            alexa_display = respuesta.get('alexa_display', 'No se pudo obtener la información.')
            
            # Usar SSML para hacer que Alexa hable más lentamente y suene más natural
            speak_output = f"<speak>{alexa_speak}</speak>"
            
            # Agregar tarjeta SimpleCard
            handler_input.response_builder.set_card(
                SimpleCard(
                    title="Clientes que han pagado",
                    content="\n".join(alexa_display)
                )
            )
            # Agregar un reprompt para mantener la sesión abierta
            reprompt_text = "¿Quieres saber algo más?"
        else:
            speak_output = "<speak>Lo siento, no pude obtener la información.</speak>"
            reprompt_text = "¿Necesitas ayuda con otra consulta?"
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)  # Indica que la sesión debe terminar
                .response  # Construye y devuelve la respuesta final
        )

APL_DOCUMENT_ID = "DineroGeneradoQuincenaActual"

APL_DOCUMENT_TOKEN = "documentToken"

DATASOURCE = {
    "headlineTemplateData": {
        "type": "object",
        "objectId": "headlineSample",
        "properties": {
            "backgroundImage": {
                "contentDescription": None,
                "smallSourceUrl": None,
                "largeSourceUrl": None,
                "sources": [
                    {
                        "url": "https://d2o906d8ln7ui1.cloudfront.net/images/templates_v3/headline/HeadlineBackground_Dark.png",
                        "size": "large"
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "type": "PlainText",
                    "text": "Welcome to The Daily Plant Facts"
                }
            },
            "logoUrl": "https://d2o906d8ln7ui1.cloudfront.net/images/templates_v3/logo/logo-modern-botanical-white.png",
            "hintText": "Try, \"Alexa, what is the plant fact of the day?\""
        }
    }
}



class PruebitaLHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("pruebita")(handler_input)

    def handle(self, handler_input):
        # Respuesta de voz
        speak_output = "Este es un ejemplo de skill con texto visible en tu app Alexa."

        # Agregar una tarjeta SimpleCard
        handler_input.response_builder.set_card(
            SimpleCard(
                title="Mi Skill con Texto",
                content="¡Hola, este es mi skill! Aquí está el mensaje que querías ver."
            )
        )

        # Retornar la respuesta
        return (
            handler_input.response_builder
                .speak(speak_output)
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
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(DineroGeneradoQuincenaActualHandler())
sb.add_request_handler(ObtenerClientesPagadosHandler())

sb.add_request_handler(PruebitaLHandler())

sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()